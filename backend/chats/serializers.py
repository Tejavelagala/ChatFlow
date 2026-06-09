from rest_framework import serializers
from .models import ChatRoom, ChatRoomMember , Message, UserProfile


class ChatRoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username'
    )
    message_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'room_id',
            'room_name',
            'owner',
            'created_at',
            'message_count',
            'member_count'
        ]
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_member_count(self, obj):
        from .models import ChatRoomMember
        return ChatRoomMember.objects.filter(room=obj).count()


class ChatRoomMemberSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = ChatRoomMember
        fields = [
            'id',
            'user',
            'room',
            'joined_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(
        source='sender.username'
    )
    file_url = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'room',
            'sender',
            'content',
            'timestamp',
            'is_seen',
            'image',
            'reactions',
            'reply_to',
            'audio',
            'file',
            'file_name',
            'file_size',
            'file_type',
            'file_url',
            'status',
            'delivered_at',
            'seen_at',
            'is_pinned',
            'pinned_at',
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

    def get_reactions(self, obj):
        from .models import MessageReaction
        from django.db.models import Count
        
        reactions = {}
        reaction_data = (
            MessageReaction.objects
            .filter(message=obj)
            .values('emoji')
            .annotate(count=Count('emoji'))
        )
        
        for item in reaction_data:
            reactions[item['emoji']] = item['count']
        
        return reactions


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
    joined_date = serializers.DateTimeField(
        source='user.date_joined',
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'avatar',
            'bio',
            'online',
            'cover_image',
            'last_active',
            'joined_date',
        ]