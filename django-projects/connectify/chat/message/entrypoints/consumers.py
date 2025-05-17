import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.message.adapters.repository import PrivateMessageRepository
from chat.message.domain.factory import PrivateChatFactory
from chat.message.service_layer.services import PrivateChatService
from chat.friend.adapters.repository import UserFriendRepository
from chat.message.service_layer.validator import PrivateChatValidator
from chat.message.service_layer import exceptions as service_layer_exceptions
from chat.message.domain import exceptions as domain_layer_exceptions


class PrivateMessageConsumer(AsyncWebsocketConsumer):


    @property
    def service(self):
        return PrivateChatService(
            message_repository=PrivateMessageRepository(),
            chat_factory=PrivateChatFactory(),
            user_friend_repository=UserFriendRepository(),
            validator=PrivateChatValidator()
        )

    async def connect(self):
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            f"user_{self.user.id}",
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")
            match action:
                case "send_message":
                    await self.handle_send_message(data)
                case "update_message":
                    await self.handle_update_message(data)
                case "mark_message_as_seen":
                    await self.handle_mark_message_as_seen(data)
                case "delete_message":
                    await self.handle_delete_message(data)
                case _:
                    await self.send(text_data=json.dumps({"error": "Invalid action", "status": 400}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON", "status": 400}))

    async def disconnect(self, close_code):
        if hasattr(self, 'user'):
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )


    async def send_to_other_channel(self, receiver_id: int, response_data: str):
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            response_data
        )

    async def handle_send_message(self, data):
        response_data = await self.save_message(
            sender_id=self.user.id,
            receiver_id=data.get('receiver_id'),
            content=data.get('content')
        )
        await self.send(text_data=json.dumps(response_data))
        await self.send_to_other_channel(
            receiver_id=data.get('receiver_id'),
            response_data=response_data
        )


    async def handle_update_message(self, data):
        response_data = await self.update_message(
            sender_id=self.user.id,
            receiver_id=data.get('receiver_id'),
            message_id=data.get('message_id'),
            content=data.get('content')
        )
        await self.send(text_data=json.dumps(response_data))

    async def handle_mark_message_as_seen(self, data):
        await self.mark_message_as_seen(
            receiver_id=self.user.id,
            message_ids=data.get('message_ids')
        )
        await self.send(text_data=json.dumps({"message": "Messages marked as seen.", "status": 200}))

    async def handle_delete_message(self, data):
        await self.delete_message(
            sender_id=self.user.id,
            message_id=data.get('message_id')
        )
        await self.send(text_data=json.dumps({"message": "Message deleted.", "status": 200}))

    @database_sync_to_async
    def save_message(self, sender_id: int, receiver_id: int, content: str):
        try:
            response_data = self.service.save_message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content
            )
            response_data['created_at'] = response_data['created_at'].isoformat()
            response_data['updated_at'] = response_data['updated_at'].isoformat()
            return {
                "message": "Message sent successfully.",
                "data": response_data,
                "status": 200
            }
        except (
            service_layer_exceptions.UserBlocked, 
            service_layer_exceptions.UserFriendRequestPending,
            service_layer_exceptions.UserFriendRequestRejected,
            domain_layer_exceptions.InvalidMessageLength
        ) as e:
            return {
                "error": str(e),
                "status": 400
            }

    @database_sync_to_async
    def update_message(self, sender_id: int, receiver_id: int, message_id: int, content: str):
        try:
            self.service.update_message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_id=message_id,
                content=content
            )
            return {
                "message": "Message updated successfully.",
                "status": 200
            }
        except (
            service_layer_exceptions.MessageNotFound,
            service_layer_exceptions.UserNotSender,
            domain_layer_exceptions.InvalidMessageLength
        ) as e:
            return {
                "error": str(e),
                "status": 400
            }


    @database_sync_to_async
    def mark_message_as_seen(self, receiver_id: int, message_ids: list):
        self.service.mark_message_as_seen(
            receiver_id=receiver_id,
            message_ids=message_ids
        )

    @database_sync_to_async
    def delete_message(self, sender_id: int, message_id: int):
        try:
            self.service.delete_message(
                sender_id=sender_id,
                message_id=message_id
            )
        except (
            service_layer_exceptions.MessageNotFound,
            service_layer_exceptions.UserNotSender
        ) as e:
            return {
                "error": str(e),
                "status": 400
            }


class PublicMessageConsumer(AsyncWebsocketConsumer):
    """Not Implemented"""