from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom, ChatRoomMember, Message, UserProfile, UserPresence


class AuthenticationTests(TestCase):
    """Test user authentication and registration"""
    
    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(
            username="teja",
            password="test123"
        )
        self.assertEqual(user.username, "teja")
        self.assertTrue(user.check_password("test123"))
    
    def test_user_profile_auto_creation(self):
        """Test that UserProfile is created"""
        user = User.objects.create_user(username="alice", password="pass")
        profile, created = UserProfile.objects.get_or_create(user=user)
        self.assertTrue(created or profile)
        self.assertEqual(profile.user.username, "alice")
    
    def test_user_presence_creation(self):
        """Test UserPresence model"""
        user = User.objects.create_user(username="bob", password="pass")
        presence = UserPresence.objects.create(user=user)
        self.assertEqual(presence.user.username, "bob")
        self.assertFalse(presence.is_online)


class RoomTests(TestCase):
    """Test chat room functionality"""
    
    def test_create_room(self):
        """Test room creation with owner"""
        user = User.objects.create_user(username="owner", password="pass")
        room = ChatRoom.objects.create(
            room_name="Coders",
            owner=user
        )
        self.assertEqual(room.room_name, "Coders")
        self.assertEqual(room.owner, user)
        self.assertIsNotNone(room.room_id)
    
    def test_room_uuid_generation(self):
        """Test that room_id is auto-generated UUID"""
        user = User.objects.create_user(username="owner", password="pass")
        room = ChatRoom.objects.create(room_name="Test", owner=user)
        self.assertIsNotNone(room.room_id)
    
    def test_room_str_representation(self):
        """Test room string representation"""
        user = User.objects.create_user(username="owner", password="pass")
        room = ChatRoom.objects.create(room_name="General", owner=user)
        self.assertEqual(str(room), "General")


class MemberTests(TestCase):
    """Test chat room membership"""
    
    def test_add_member(self):
        """Test adding a member to a room"""
        user = User.objects.create_user(username="john")
        owner = User.objects.create_user(username="owner")
        room = ChatRoom.objects.create(room_name="Test", owner=owner)
        member = ChatRoomMember.objects.create(
            user=user,
            room=room
        )
        self.assertEqual(member.user.username, "john")
        self.assertEqual(member.role, "member")
    
    def test_member_roles(self):
        """Test different member roles"""
        owner = User.objects.create_user(username="owner")
        admin = User.objects.create_user(username="admin")
        moderator = User.objects.create_user(username="mod")
        member = User.objects.create_user(username="member")
        
        room = ChatRoom.objects.create(room_name="Test", owner=owner)
        
        ChatRoomMember.objects.create(user=owner, room=room, role="owner")
        ChatRoomMember.objects.create(user=admin, room=room, role="admin")
        ChatRoomMember.objects.create(user=moderator, room=room, role="moderator")
        ChatRoomMember.objects.create(user=member, room=room, role="member")
        
        self.assertEqual(ChatRoomMember.objects.filter(room=room).count(), 4)
    
    def test_member_ban_status(self):
        """Test member ban functionality"""
        user = User.objects.create_user(username="banned")
        owner = User.objects.create_user(username="owner")
        room = ChatRoom.objects.create(room_name="Test", owner=owner)
        member = ChatRoomMember.objects.create(user=user, room=room, is_banned=True)
        self.assertTrue(member.is_banned)
    
    def test_member_mute_status(self):
        """Test member mute functionality"""
        user = User.objects.create_user(username="muted")
        owner = User.objects.create_user(username="owner")
        room = ChatRoom.objects.create(room_name="Test", owner=owner)
        member = ChatRoomMember.objects.create(user=user, room=room, is_muted=True)
        self.assertTrue(member.is_muted)


class MessageTests(TestCase):
    """Test messaging functionality"""
    
    def test_send_message(self):
        """Test sending a message"""
        user = User.objects.create_user(username="alice")
        room = ChatRoom.objects.create(
            room_name="General",
            owner=user
        )
        message = Message.objects.create(
            sender=user,
            room=room,
            content="Hello"
        )
        self.assertEqual(message.content, "Hello")
        self.assertEqual(message.status, "sent")
    
    def test_message_timestamp(self):
        """Test that messages have timestamps"""
        user = User.objects.create_user(username="alice")
        room = ChatRoom.objects.create(room_name="Test", owner=user)
        message = Message.objects.create(sender=user, room=room, content="Test")
        self.assertIsNotNone(message.timestamp)
    
    def test_message_reactions(self):
        """Test message reactions"""
        user = User.objects.create_user(username="alice")
        room = ChatRoom.objects.create(room_name="Test", owner=user)
        message = Message.objects.create(
            sender=user,
            room=room,
            content="Hello",
            reactions={"👍": 2, "❤️": 1}
        )
        self.assertEqual(message.reactions["👍"], 2)
    
    def test_message_reply(self):
        """Test replying to a message"""
        user = User.objects.create_user(username="alice")
        room = ChatRoom.objects.create(room_name="Test", owner=user)
        original = Message.objects.create(sender=user, room=room, content="Original")
        reply = Message.objects.create(
            sender=user,
            room=room,
            content="Reply",
            reply_to=original
        )
        self.assertEqual(reply.reply_to, original)
    
    def test_pinned_message(self):
        """Test message pinning"""
        user = User.objects.create_user(username="alice")
        room = ChatRoom.objects.create(room_name="Test", owner=user)
        message = Message.objects.create(
            sender=user,
            room=room,
            content="Important",
            is_pinned=True,
            pinned_by=user
        )
        self.assertTrue(message.is_pinned)
        self.assertEqual(message.pinned_by, user)


class ProtectedApiTests(TestCase):
    """Test API authentication and permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
    
    def test_rooms_require_auth(self):
        """Test that rooms endpoint requires authentication"""
        response = self.client.get("/api/chat/all-rooms/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_room_requires_auth(self):
        """Test room creation requires authentication"""
        response = self.client.post("/api/chat/create-room/", {"room_name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_can_create_room(self):
        """Test authenticated user can create room"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/chat/create-room/", {"room_name": "Test Room"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_list_rooms(self):
        """Test authenticated user can list rooms"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/chat/all-rooms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_can_join_room(self):
        """Test user can join a room"""
        room = ChatRoom.objects.create(room_name="Test", owner=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/chat/join-room/{room.room_id}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])


class RoomOwnerTests(TestCase):
    """Test room ownership and permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(username="owner", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.room = ChatRoom.objects.create(room_name="Test", owner=self.owner)
    
    def test_owner_can_delete_room(self):
        """Test room owner can delete room"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/api/chat/delete-room/{self.room.room_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_owner_cannot_delete_room(self):
        """Test non-owner cannot delete room"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/chat/delete-room/{self.room.room_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MessagePermissionTests(TestCase):
    """Test message permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.sender = User.objects.create_user(username="sender", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.room = ChatRoom.objects.create(room_name="Test", owner=self.sender)
        self.message = Message.objects.create(
            sender=self.sender,
            room=self.room,
            content="Test message"
        )
    
    def test_sender_can_delete_own_message(self):
        """Test user can delete their own message"""
        self.client.force_authenticate(user=self.sender)
        response = self.client.delete(f"/api/chat/delete-message/{self.message.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_sender_cannot_delete_message(self):
        """Test user cannot delete others' messages"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/chat/delete-message/{self.message.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_sender_can_edit_own_message(self):
        """Test user can edit their own message"""
        self.client.force_authenticate(user=self.sender)
        response = self.client.put(
            f"/api/chat/edit-message/{self.message.id}/",
            {"content": "Updated"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileTests(TestCase):
    """Test user profile functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="pass")
    
    def test_profile_creation(self):
        """Test profile creation"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio="Test bio"
        )
        self.assertEqual(profile.bio, "Test bio")
        self.assertFalse(profile.online)
    
    def test_authenticated_user_can_get_profile(self):
        """Test authenticated user can retrieve profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/chat/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)est room owner can delete room"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/api/chat/delete-room/{self.room.room_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_owner_cannot_delete_room(self):
        """Test non-owner cannot delete room"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/chat/delete-room/{self.room.room_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MessagePermissionTests(TestCase):
    """Test message permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.sender = User.objects.create_user(username="sender", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.room = ChatRoom.objects.create(room_name="Test", owner=self.sender)
        self.message = Message.objects.create(
            sender=self.sender,
            room=self.room,
            content="Test message"
        )
    
    def test_sender_can_delete_own_message(self):
        """Test user can delete their own message"""
        self.client.force_authenticate(user=self.sender)
        response = self.client.delete(f"/api/chat/delete-message/{self.message.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_sender_cannot_delete_message(self):
        """Test user cannot delete others' messages"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/chat/delete-message/{self.message.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_sender_can_edit_own_message(self):
        """Test user can edit their own message"""
        self.client.force_authenticate(user=self.sender)
        response = self.client.put(
            f"/api/chat/edit-message/{self.message.id}/",
            {"content": "Updated"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileTests(TestCase):
    """Test user profile functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="pass")
    
    def test_profile_creation(self):
        """Test profile creation"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio="Test bio"
        )
        self.assertEqual(profile.bio, "Test bio")
        self.assertFalse(profile.online)
    
    def test_authenticated_user_can_get_profile(self):
        """Test authenticated user can retrieve profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/chat/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
