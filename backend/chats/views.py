from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from .models import ChatRoom, ChatRoomMember, Message, UserProfile
from .models import UserPresence
from .serializers import (
    ChatRoomSerializer,
    ChatRoomMemberSerializer,
    MessageSerializer,
    UserProfileSerializer
)
from .validators import validate_file_upload

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_AUDIO_SIZE = 10 * 1024 * 1024
MAX_FILE_SIZE = 10 * 1024 * 1024

class MessagePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 100

class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_name = request.data.get('room_name', '').strip()
        
        if not room_name:
            return Response(
                {'error': 'Room name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(room_name) > 100:
            return Response(
                {'error': 'Room name cannot exceed 100 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        room = ChatRoom.objects.create(
            room_name=room_name,
            owner=request.user
        )
        ChatRoomMember.objects.create(
            user=request.user,
            room=room,
            role='owner'
        )
        serializer = ChatRoomSerializer(room)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        member, created = ChatRoomMember.objects.get_or_create(
            user=request.user,
            room=room
        )
        serializer = ChatRoomMemberSerializer(member)
        return Response(serializer.data)


class RoomDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)
    
@method_decorator(
    ratelimit(key='user', rate='60/m', method='POST'),
    name='post'
)
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get('content')
        message = Message.objects.create(
            room=room,
            sender=request.user,
            content=content
        )
        serializer = MessageSerializer(message)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class AllRoomsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get rooms where user is a member
        member_room_ids = ChatRoomMember.objects.filter(
            user=request.user
        ).values_list('room_id', flat=True)
        
        rooms = ChatRoom.objects.filter(id__in=member_room_ids)
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = ChatRoom.objects.get(room_id=room_id)
        messages = (
            Message.objects
            .select_related('sender', 'room')
            .filter(room=room)
            .order_by('-timestamp')
        )
        
        paginator = MessagePagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class DeleteRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_id):
        room = ChatRoom.objects.get(room_id=room_id)

        if room.owner != request.user:
            return Response(
                {'error': 'Not allowed'},
                status=403
            )

        room.delete()
        return Response({'message': 'Room deleted'})


class UserPresenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            presence = UserPresence.objects.get(user=user)
            return Response({
                'is_online': presence.is_online,
                'last_seen': presence.last_seen,
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except UserPresence.DoesNotExist:
            return Response(
                {'error': 'User presence not found'},
                status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(
    ratelimit(key='user', rate='20/m', method='POST'),
    name='post'
)
class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        room_id = request.data.get('room_id')
        image = request.FILES.get('image')

        if image and image.size > MAX_IMAGE_SIZE:
            return Response(
                {'error': f'Image size cannot exceed {MAX_IMAGE_SIZE / (1024*1024):.0f}MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            room = ChatRoom.objects.get(room_id=room_id)
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content='',
                image=image
            )
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
            
            if message.sender != request.user:
                return Response(
                    {'error': 'Not allowed'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            message.delete()
            return Response(
                {'message': 'Deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class EditMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
            
            if message.sender != request.user:
                return Response(
                    {'error': 'Not allowed'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            new_content = request.data.get('content')
            message.content = new_content
            message.save()
            
            return Response(
                {
                    'message': 'Updated successfully',
                    'content': message.content
                },
                status=status.HTTP_200_OK
            )
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ReactMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        try:
            from .models import MessageReaction
            from django.db.models import Count
            
            message = Message.objects.get(id=message_id)
            emoji = request.data.get('emoji')
            
            if not emoji:
                return Response(
                    {'error': 'Emoji required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reaction, created = MessageReaction.objects.get_or_create(
                message=message,
                user=request.user,
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
            
            return Response(
                {'reactions': reactions},
                status=status.HTTP_200_OK
            )
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )    


@method_decorator(
    ratelimit(key='user', rate='20/m', method='POST'),
    name='post'
)
class UploadAudioView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        room_id = request.data.get('room_id')
        audio = request.FILES.get('audio')

        if audio and audio.size > MAX_AUDIO_SIZE:
            return Response(
                {'error': f'Audio size cannot exceed {MAX_AUDIO_SIZE / (1024*1024):.0f}MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            room = ChatRoom.objects.get(room_id=room_id)
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content='',
                audio=audio
            )
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )
        serializer = UserProfileSerializer(profile)
        data = serializer.data
        
        # Add rooms count
        rooms_count = ChatRoomMember.objects.filter(user=request.user).count()
        data['rooms_count'] = rooms_count
        
        return Response(data)

    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )
        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(
    ratelimit(key='user', rate='20/m', method='POST'),
    name='post'
)
class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        room_id = request.data.get('room_id')
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if file.size > MAX_FILE_SIZE:
            return Response(
                {'error': f'File size cannot exceed {MAX_FILE_SIZE / (1024*1024):.0f}MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_file_upload(file)
            
            room = ChatRoom.objects.get(room_id=room_id)
            
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=f'📎 {file.name}',
                file=file
            )
            
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PinMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        try:
            from django.utils import timezone
            message = Message.objects.get(id=message_id)
            
            # Check if user is room owner or admin (add permission check later)
            if message.room.owner != request.user:
                return Response(
                    {'error': 'Only room owner can pin messages'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            message.is_pinned = True
            message.pinned_at = timezone.now()
            message.pinned_by = request.user
            message.save()
            
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UnpinMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
            
            if message.room.owner != request.user:
                return Response(
                    {'error': 'Only room owner can unpin messages'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            message.is_pinned = False
            message.pinned_at = None
            message.pinned_by = None
            message.save()
            
            return Response(
                {'message': 'Message unpinned successfully'},
                status=status.HTTP_200_OK
            )
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PinnedMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            pinned_messages = (
                Message.objects
                .select_related('sender', 'room')
                .filter(room=room, is_pinned=True)
                .order_by('-pinned_at')
            )
            
            serializer = MessageSerializer(
                pinned_messages,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class RoomMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            members = (
                ChatRoomMember.objects
                .select_related('user')
                .filter(room=room)
            )
            
            data = [
                {
                    'username': member.user.username,
                    'role': member.role,
                    'is_banned': member.is_banned,
                    'is_muted': member.is_muted,
                    'joined_at': member.joined_at
                }
                for member in members
            ]
            
            return Response(data)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class LeaveRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Prevent room owner from leaving
            if room.owner == request.user:
                return Response(
                    {'error': 'Room owner cannot leave room'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ChatRoomMember.objects.filter(
                room=room,
                user=request.user
            ).delete()
            
            return Response({
                'message': 'Left room successfully'
            })
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PromoteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            username = request.data.get('username')
            role = request.data.get('role')
            
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Check if requester is owner
            owner = ChatRoomMember.objects.get(
                room=room,
                user=request.user
            )
            
            if owner.role != 'owner':
                return Response(
                    {'error': 'Only owner can promote users'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            target_user = User.objects.get(username=username)
            
            member = ChatRoomMember.objects.get(
                room=room,
                user=target_user
            )
            
            member.role = role
            member.save()
            
            return Response({
                'message': f'User promoted to {role}'
            })
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ChatRoomMember.DoesNotExist:
            return Response(
                {'error': 'User is not a member of this room'},
                status=status.HTTP_404_NOT_FOUND
            )


class BanUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            username = request.data.get('username')
            
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Check permissions (owner or admin)
            requester = ChatRoomMember.objects.get(
                room=room,
                user=request.user
            )
            
            if requester.role not in ['owner', 'admin']:
                return Response(
                    {'error': 'Only owners and admins can ban users'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            target_user = User.objects.get(username=username)
            
            member = ChatRoomMember.objects.get(
                room=room,
                user=target_user
            )
            
            member.is_banned = True
            member.save()
            
            return Response({
                'message': 'User banned successfully'
            })
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ChatRoomMember.DoesNotExist:
            return Response(
                {'error': 'User is not a member of this room'},
                status=status.HTTP_404_NOT_FOUND
            )


class MuteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            username = request.data.get('username')
            
            room = ChatRoom.objects.get(room_id=room_id)
            
            # Check permissions (owner, admin, or moderator)
            requester = ChatRoomMember.objects.get(
                room=room,
                user=request.user
            )
            
            if requester.role not in ['owner', 'admin', 'moderator']:
                return Response(
                    {'error': 'Only owners, admins, and moderators can mute users'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            target_user = User.objects.get(username=username)
            
            member = ChatRoomMember.objects.get(
                room=room,
                user=target_user
            )
            
            member.is_muted = True
            member.save()
            
            return Response({
                'message': 'User muted successfully'
            })
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ChatRoomMember.DoesNotExist:
            return Response(
                {'error': 'User is not a member of this room'},
                status=status.HTTP_404_NOT_FOUND
            )
