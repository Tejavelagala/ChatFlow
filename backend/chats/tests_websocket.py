from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken
from config.asgi import application
from chats.models import ChatRoom, ChatRoomMember


class WebSocketTests(TransactionTestCase):
    """Test WebSocket connections and messaging"""
    
    async def test_unauthenticated_connection_rejected(self):
        """Test that unauthenticated connections are rejected"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass"
        )
        room = await database_sync_to_async(ChatRoom.objects.create)(
            room_name="Test Room",
            owner=user
        )
        
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.room_id}/testuser/"
        )
        connected, _ = await communicator.connect()
        
        # Should reject without authentication
        self.assertFalse(connected)
        await communicator.disconnect()
    
    async def test_invalid_room_rejected(self):
        """Test that invalid room IDs are handled"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass"
        )
        token = str(AccessToken.for_user(user))

        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/invalid-uuid/testuser/?token={token}"
        )
        connected, _ = await communicator.connect()
        
        # Should reject invalid room
        self.assertFalse(connected)
        await communicator.disconnect()


class WebSocketMessageTests(TransactionTestCase):
    """Test WebSocket messaging functionality"""
    
    async def test_ping_pong(self):
        """Test ping/pong heartbeat"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass"
        )
        room = await database_sync_to_async(ChatRoom.objects.create)(
            room_name="Test Room",
            owner=user
        )
        await database_sync_to_async(ChatRoomMember.objects.create)(
            user=user,
            room=room
        )
        token = str(AccessToken.for_user(user))
        
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.room_id}/testuser/?token={token}"
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        online_users = await communicator.receive_json_from()
        self.assertEqual(online_users.get("type"), "online_users")

        await communicator.send_json_to({"type": "ping"})
        response = await communicator.receive_json_from()
        self.assertEqual(response.get("type"), "pong")
        
        await communicator.disconnect()


class WebSocketConnectionTests(TransactionTestCase):
    """Test WebSocket connection handling"""
    
    async def test_connection_with_valid_user(self):
        """Test connection with valid authenticated user"""
        user = await database_sync_to_async(User.objects.create_user)(
            username="validuser",
            password="testpass"
        )
        room = await database_sync_to_async(ChatRoom.objects.create)(
            room_name="Test Room",
            owner=user
        )
        await database_sync_to_async(ChatRoomMember.objects.create)(
            user=user,
            room=room
        )
        token = str(AccessToken.for_user(user))
        
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.room_id}/validuser/?token={token}"
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)
        
        await communicator.disconnect()
