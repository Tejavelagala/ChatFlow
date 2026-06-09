# Add to consumers.py receive method

async def receive(self, text_data):
    # ... existing code ...
    
    # REACTION EVENT
    elif event_type == 'reaction':
        message_id = data.get('message_id')
        emoji = data.get('emoji')
        if not message_id or not emoji:
            await self.send_error('Message ID and emoji required')
            return
        
        try:
            reactions = await self.add_reaction(message_id, emoji)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reaction_event',
                    'message_id': message_id,
                    'reactions': reactions
                }
            )
        except Exception as e:
            logger.error(f'Failed to add reaction: {e}')
        return

@sync_to_async
def add_reaction(self, message_id, emoji):
    from .models import Message
    message = Message.objects.get(id=message_id)
    reactions = message.reactions
    reactions[emoji] = reactions.get(emoji, 0) + 1
    message.reactions = reactions
    message.save()
    return reactions

async def reaction_event(self, event):
    await self.send(text_data=json.dumps({
        'type': 'reaction',
        'message_id': event['message_id'],
        'reactions': event['reactions']
    }))
