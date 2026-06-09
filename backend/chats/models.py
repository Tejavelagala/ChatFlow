from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid

class UserProfile(models.Model):

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE
    )

    avatar = models.ImageField(

        upload_to='avatars/',

        null=True,

        blank=True
    )

    bio = models.TextField(

        blank=True,

        max_length=250
    )

    online = models.BooleanField(

        default=False
    )

    cover_image = models.ImageField(

        upload_to='covers/',

        null=True,

        blank=True
    )

    last_active = models.DateTimeField(

        auto_now=True
    )

    def __str__(self):

        return self.user.username

class UserPresence(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    last_seen = models.DateTimeField(
        auto_now=True
    )

    is_online = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    room_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    room_name = models.CharField(
        max_length=100
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_rooms'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.room_name


class ChatRoomMember(models.Model):

    ROLE_CHOICES = [

        ('owner', 'Owner'),

        ('admin', 'Admin'),

        ('moderator', 'Moderator'),

        ('member', 'Member'),
    ]

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE
    )

    room = models.ForeignKey(

        ChatRoom,

        on_delete=models.CASCADE
    )

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES,

        default='member'
    )

    is_banned = models.BooleanField(
        default=False
    )

    is_muted = models.BooleanField(
        default=False
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'room')
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['user']),
        ]

class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='chat_images/',
        null=True,
        blank=True
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    is_seen = models.BooleanField(
        default=False
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )

    audio = models.FileField(
        upload_to='chat_audio/',
        null=True,
        blank=True
   )

    # FILE SHARING FIELDS
    file = models.FileField(
        upload_to='chat_files/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf', 'doc', 'docx', 'txt', 'zip',
                    'rar', 'xlsx', 'pptx', 'csv'
                ]
            )
        ]
    )
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)

    # MESSAGE STATUS FIELDS
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('seen', 'Seen'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='sent'
    )
    
    delivered_at = models.DateTimeField(null=True, blank=True)
    seen_at = models.DateTimeField(null=True, blank=True)
    seen_by = models.ManyToManyField(
        User,
        related_name='seen_messages',
        blank=True
    )

    # PINNED MESSAGE
    is_pinned = models.BooleanField(default=False)
    pinned_at = models.DateTimeField(null=True, blank=True)
    pinned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pinned_messages'
    )

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['room', '-timestamp']),
            models.Index(fields=['sender']),
        ]

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'


class MessageReaction(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_reactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user', 'emoji')
        indexes = [
            models.Index(fields=['message']),
        ]

    def __str__(self):
        return f'{self.user.username} reacted {self.emoji} to message {self.message.id}'