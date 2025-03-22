import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import User
from .models import ChatSession, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat functionality.
    Uses Django Channels to manage WebSocket connections, receive messages,
    and broadcast them to the appropriate chat room.
    """

    async def connect(self):
        """
        Handle new WebSocket connections.
        Join the WebSocket connection to the appropriate chat room group.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Add the channel to the chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Accept the WebSocket connection

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Remove the WebSocket connection from the chat room group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive a message from the WebSocket.
        Broadcast the message to the chat group and save it to the database.
        """
        try:
            data = json.loads(text_data)
            message = data['message']
            username = data['username']
            room = data['room']

            # Save the received message to the database
            await self.save_message(username, room, message)

            # Broadcast the message to the chat group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )

        except KeyError as e:
            # Handle missing fields in the incoming message data
            print(f"Missing key in message data: {e}")
        except json.JSONDecodeError as e:
            # Handle invalid JSON structure
            print(f"Invalid JSON received: {e}")

    async def chat_message(self, event):
        """
        Receive a message event from the chat group and send it to WebSocket.
        """
        message = event['message']
        username = event['username']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        """
        Save a message to the database.
        This function is run asynchronously to avoid blocking the event loop.
        """
        try:
            # Get user and chat session instances
            user = User.objects.get(username=username)
            chat_session = ChatSession.objects.get(name=room)

            # Create a new message record
            Message.objects.create(chat_session=chat_session, user=user, message=message)
        except User.DoesNotExist:
            print(f"User with username {username} does not exist.")
        except ChatSession.DoesNotExist:
            print(f"Chat session with room name {room} does not exist.")
