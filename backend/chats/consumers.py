import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import ChatRoom, ChatRoomMember, UserPresence

logger = logging.getLogger(__name__)

# Store online users per room: {room_id: set(usernames)}
online_users_by_room = {}

class ChatConsumer(AsyncWebsocketConsumer):

    async def send_error(self, message):
        """Send error message to client"""
        try:
            await self.send(
                text_data=json.dumps({
                    'type': 'error',
                    'message': message
                })
            )
        except Exception as e:
            logger.error(f'Failed to send error message: {e}')

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs'].get('room_id')
        requested_username = self.scope['url_route']['kwargs'].get('username')
        client = self.scope.get('client')

        try:
            user = self.scope.get('user')
            logger.debug(
                "WSCONNECTING room=%s requested_username=%s client=%s user=%s authenticated=%s",
                self.room_id,
                requested_username,
                client,
                getattr(user, 'username', None),
                bool(user and user.is_authenticated),
            )
            
            if not user or not user.is_authenticated:
                logger.warning(
                    "WSREJECT code=4401 reason=auth_failed room=%s requested_username=%s client=%s user_class=%s",
                    self.room_id,
                    requested_username,
                    client,
                    user.__class__.__name__ if user else None,
                )
                await self.close(code=4401)
                return

            self.user = user
            self.username = user.username
            
            # Check username match (case-sensitive)
            if requested_username and requested_username != self.username:
                logger.warning(
                    "WSREJECT code=4403 reason=username_mismatch room=%s requested_username='%s' token_username='%s' match=%s client=%s",
                    self.room_id,
                    requested_username,
                    self.username,
                    requested_username.lower() == self.username.lower(),
                    client,
                )
                await self.close(code=4403)
                return

            has_access, access_reason = await self.get_room_access(user.id, self.room_id)
            
            if not has_access:
                logger.warning(
                    "WSREJECT code=4403 reason=%s room=%s username=%s client=%s",
                    access_reason,
                    self.room_id,
                    self.username,
                    client,
                )
                await self.close(code=4403)
                return

            self.room_group_name = f'chat_{self.room_id}'

            # Verify channel layer is working
            if not self.channel_layer:
                logger.error(
                    "WSREJECT code=4500 reason=no_channel_layer room=%s username=%s",
                    self.room_id,
                    self.username,
                )
                await self.close(code=4500)
                return

            logger.debug(
                "REDIS attempting group_add group=%s channel=%s",
                self.room_group_name,
                self.channel_name,
            )

            try:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                logger.debug(
                    "REDIS group_add success group=%s channel=%s",
                    self.room_group_name,
                    self.channel_name,
                )
            except Exception as e:
                logger.exception(
                    "WSREJECT code=4500 reason=redis_group_add_failed group=%s channel=%s error=%s",
                    self.room_group_name,
                    self.channel_name,
                    str(e),
                )
                await self.close(code=4500)
                return

            await self.accept()
            logger.info(
                "WSACCEPT room=%s username=%s access=%s channel=%s",
                self.room_id,
                self.username,
                access_reason,
                self.channel_name,
            )

            # Add user to room-specific online set (convert UUID to string for dict key)
            room_key = str(self.room_id)
            if room_key not in online_users_by_room:
                online_users_by_room[room_key] = set()
            online_users_by_room[room_key].add(self.username)

            try:
                logger.debug(
                    "REDIS broadcasting online_users group=%s room=%s users_count=%d users=%s",
                    self.room_group_name,
                    room_key,
                    len(online_users_by_room[room_key]),
                    list(online_users_by_room[room_key]),
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'online_users_event',
                        'users': list(online_users_by_room[room_key]),
                    }
                )
                logger.debug(
                    "REDIS online_users broadcast success group=%s",
                    self.room_group_name,
                )
            except Exception as e:
                logger.exception(
                    "WSERROR reason=online_users_broadcast_failed group=%s error=%s",
                    self.room_group_name,
                    str(e),
                )
        except Exception as e:
            logger.exception(
                "WSREJECT code=4500 reason=connect_exception room=%s requested_username=%s client=%s error=%s",
                self.room_id,
                requested_username,
                client,
                e,
            )
            await self.close(code=4500)

    async def disconnect(self, close_code):
        logger.info(
            "WSDISCONNECT code=%s room=%s username=%s",
            close_code,
            getattr(self, 'room_id', 'unknown'),
            getattr(self, 'username', 'unknown'),
        )
        
        try:
            room_group_name = getattr(self, 'room_group_name', None)
            if room_group_name:
                logger.debug(
                    "REDIS group_discard group=%s channel=%s",
                    room_group_name,
                    self.channel_name,
                )
                await self.channel_layer.group_discard(
                    room_group_name,
                    self.channel_name
                )

            username = getattr(self, 'username', None)
            room_id = getattr(self, 'room_id', None)
            
            # Remove user from room-specific online set (convert UUID to string)
            room_key = str(room_id) if room_id else None
            if room_key and room_key in online_users_by_room:
                if username in online_users_by_room[room_key]:
                    online_users_by_room[room_key].remove(username)
                    logger.debug(
                        "PRESENCE user removed username=%s room=%s online_count=%d",
                        username,
                        room_key,
                        len(online_users_by_room[room_key]),
                    )

                    if room_group_name:
                        await self.channel_layer.group_send(
                            room_group_name,
                            {
                                'type': 'online_users_event',
                                'users': list(online_users_by_room[room_key]),
                            }
                        )
                    
                    # Clean up empty room sets
                    if not online_users_by_room[room_key]:
                        del online_users_by_room[room_key]
        except Exception as e:
            logger.exception(
                "WSDISCONNECT error code=%s error=%s",
                close_code,
                str(e),
            )

    async def online_users_event(self, event):
        """Handle online users broadcast event"""
        try:
            users = event.get('users', [])
            logger.debug(
                "ONLINE_USERS_EVENT sending to client username=%s users=%s",
                getattr(self, 'username', 'unknown'),
                users,
            )
            await self.send(
                text_data=json.dumps({
                    'type': 'online_users',
                    'users': users,
                })
            )
        except Exception as e:
            logger.error(
                "ONLINE_USERS_EVENT error username=%s error=%s",
                getattr(self, 'username', 'unknown'),
                str(e),
            )        
            


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON received: {e}')
            await self.send_error('Invalid JSON format')
            return
        except Exception as e:
            logger.error(f'JSON parsing error: {e}')
            await self.send_error('Error processing message')
            return

        try:
            event_type = data.get('type')
            username = getattr(self, 'username', None)

            # HEARTBEAT PING
            if event_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong'
                }))
                return

            # CHAT MESSAGE
            if event_type == 'message':
                message = data.get('message')
                if not message:
                    await self.send_error('Message content required')
                    return
                
                # Check if user is muted
                is_muted = await self.check_if_muted(self.user.id, self.room_id)
                if is_muted:
                    await self.send_error('You are muted in this room')
                    return
                    
                try:
                    logger.debug(
                        "MSG_SEND saving message room=%s username=%s length=%d",
                        self.room_id,
                        username,
                        len(message),
                    )
                    message_id = await self.save_message(username, self.room_id, message)
                    
                    logger.debug(
                        "MSG_SEND broadcasting message_id=%s group=%s",
                        message_id,
                        self.room_group_name,
                    )
                    
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'username': username,
                            'message_id': message_id,
                            'created_at': str(timezone.now())
                        }
                    )
                    
                    logger.debug(
                        "MSG_SEND broadcast success message_id=%s group=%s",
                        message_id,
                        self.room_group_name,
                    )
                except Exception as e:
                    logger.exception(
                        "MSG_SEND failed room=%s username=%s error=%s",
                        self.room_id,
                        username,
                        str(e),
                    )
                    await self.send_error('Failed to save message')
                return

            # TYPING EVENT
            elif event_type == 'typing':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_event',
                        'username': username,
                    }
                )

            # MESSAGE DELIVERED
            elif event_type == 'delivered':
                message_id = data.get('message_id')
                if not message_id:
                    await self.send_error('Message ID required')
                    return
                    
                try:
                    await self.mark_message_delivered(message_id)
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'message_delivered',
                            'message_id': message_id,
                            'delivered_at': str(timezone.now())
                        }
                    )
                except Exception as e:
                    logger.error(f'Failed to mark message delivered: {e}')
                return

            # SEEN EVENT
            elif event_type == 'seen':
                message_id = data.get('message_id')
                if not message_id:
                    await self.send_error('Message ID required')
                    return
                    
                try:
                    await self.mark_message_seen(message_id, username)
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'seen_event',
                            'message_id': message_id,
                            'seen_by': username,
                            'seen_at': str(timezone.now())
                        }
                    )
                except Exception as e:
                    logger.error(f'Failed to mark message seen: {e}')
                return

            # REACTION EVENT
            elif event_type == 'reaction':
                message_id = data.get('message_id')
                emoji = data.get('emoji')
                if not message_id or not emoji:
                    await self.send_error('Message ID and emoji required')
                    return
                    
                try:
                    reactions = await self.toggle_reaction(message_id, username, emoji)
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'reaction_event',
                            'message_id': message_id,
                            'reactions': reactions
                        }
                    )
                except Exception as e:
                    logger.error(f'Failed to toggle reaction: {e}')
                return
        except Exception as e:
            logger.error(f'WebSocket receive error: {e}')
            await self.send_error('Error processing request')

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        message_id = event.get('message_id')
        created_at = event.get('created_at')

        await self.send(
            text_data=json.dumps({
                'message': message,
                'username': username,
                'message_id': message_id,
                'created_at': created_at
            })
        )

    async def typing_event(self, event):
        
        await self.send(
            text_data=json.dumps({
                'type': 'typing',
                'username': event['username'],
            })
        )

    @sync_to_async
    def get_room_access(self, user_id, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except (ChatRoom.DoesNotExist, ValidationError, ValueError):
            return False, 'room_not_found'

        if room.owner_id == user_id:
            return True, 'owner'

        member = ChatRoomMember.objects.filter(
            room=room,
            user_id=user_id
        ).first()

        if not member:
            return False, 'not_room_member'

        if member.is_banned:
            return False, 'banned_member'

        return True, f'member:{member.role}'

    @sync_to_async
    def check_if_muted(self, user_id, room_id):
        """
        Check if user is muted in the room.
        Returns True if user is muted OR not a member.
        Returns False only if user is owner or unmuted member.
        """
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Owner bypass - owner can never be muted
            if room.owner_id == user_id:
                return False
            
            # Check member status
            member = ChatRoomMember.objects.filter(
                room=room,
                user_id=user_id
            ).first()
            
            # Not a member = no permission to send
            if not member:
                logger.warning(
                    f"User {user_id} attempted to send but is not a member of room {room_id}"
                )
                return True
            
            # Return actual mute status
            return member.is_muted
            
        except ChatRoom.DoesNotExist:
            logger.error(f'Room {room_id} does not exist in check_if_muted')
            return True
        except Exception as e:
            logger.error(f'Error in check_if_muted: {e}')
            return True

    @sync_to_async
    def save_message(self, username, room_id, message):
        from .models import Message

        room = ChatRoom.objects.get(room_id=room_id)
        message_obj = Message.objects.create(
            room=room,
            sender=self.user,
            content=message
        )
        return message_obj.id

    @sync_to_async
    def mark_message_seen(self, message_id, username):
        try:
            from .models import Message
            message = Message.objects.get(id=message_id)
            message.seen_by.add(self.user)
            message.status = 'seen'
            message.seen_at = timezone.now()
            message.is_seen = True
            message.save()
        except Exception as e:
            logger.error(f'Error marking message seen: {e}')

    @sync_to_async
    def mark_message_delivered(self, message_id):
        try:
            from .models import Message
            message = Message.objects.get(id=message_id)
            if message.status == 'sent':
                message.status = 'delivered'
                message.delivered_at = timezone.now()
                message.save()
        except Exception as e:
            logger.error(f'Error marking message delivered: {e}')

    async def message_delivered(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delivered',
            'message_id': event['message_id'],
            'delivered_at': event['delivered_at']
        }))

    async def seen_event(self, event):
        await self.send(
            text_data=json.dumps({
                'type': 'seen',
                'message_id': event['message_id'],
                'seen_by': event.get('seen_by'),
                'seen_at': event.get('seen_at')
            })
        )

    async def reaction_event(self, event):
        await self.send(
            text_data=json.dumps({
                'type': 'reaction',
                'message_id': event['message_id'],
                'reactions': event['reactions']
            })
        )

    @sync_to_async
    def set_user_online(self,username):

       from django.contrib.auth.models import User

       user = User.objects.get( username=username)
       presence, created = (UserPresence.objects.get_or_create(user=user))

       presence.is_online = True

       presence.save()


    @sync_to_async
    def set_user_offline(self,username):

        from django.contrib.auth.models import User

        user = User.objects.get(username=username)

        presence, created = (
        UserPresence.objects.get_or_create(user=user ))

        presence.is_online = False

        presence.save()

    @sync_to_async
    def toggle_reaction(self, message_id, username, emoji):
        from .models import Message, MessageReaction
        from django.contrib.auth.models import User
        from django.db.models import Count

        message = Message.objects.get(id=message_id)
        user = User.objects.get(username=username)

        reaction, created = MessageReaction.objects.get_or_create(
            message=message,
            user=user,
            emoji=emoji
        )

        if not created:
            reaction.delete()

        reactions = {}
        reaction_data = (
            MessageReaction.objects
            .filter(message=message)
            .values('emoji')
            .annotate(count=Count('emoji'))
        )
        
        for item in reaction_data:
            reactions[item['emoji']] = item['count']

        return reactions
