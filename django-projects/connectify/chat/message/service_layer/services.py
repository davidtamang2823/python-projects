from abc import ABC, abstractmethod
from typing import List
from django.db.transaction import atomic
from chat.message.adapters.repository import AbstractPrivateMessageRepository
from chat.message.domain.factory import AbstractPrivateChatFactory
from chat.friend.adapters.repository import AbstractUserFriendRepository
from chat.message.service_layer.validator import PrivateChatValidator

class AbstractPrivateChatService(ABC):


    @abstractmethod
    def get_messages_between_users(self, sender_id: int, reciver_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_recent_messages(self, receiver_id: int):
        raise NotImplementedError

    @abstractmethod
    def save_message(self, sender_id: int, receiver_id: int, content: str):
        raise NotImplementedError

    @abstractmethod
    def update_message(self, sender_id: int, reciever_id: int, message_id: int, content: str):
        raise NotImplementedError

    @abstractmethod
    def mark_message_as_seen(self, reciever_id:int, message_ids: List[int]):
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, sender_id: int, message_ids: int):
        raise NotImplementedError


class PrivateChatService(AbstractPrivateChatService):


    def __init__(
        self, 
        message_repository: AbstractPrivateMessageRepository, 
        chat_factory: AbstractPrivateChatFactory, 
        user_friend_repository: AbstractUserFriendRepository,
        validator: PrivateChatValidator
    ):
        self.user_friend_repository = user_friend_repository
        self.chat_factory = chat_factory
        self.message_repository = message_repository
        self.validator = validator


    def get_messages_between_users(self, sender_id: int, receiver_id: int):
        return self.message_repository.get_messages_between_users(
            sender_id=sender_id, 
            receiver_id=receiver_id
        )

    def get_recent_messages(self, receiver_id: int):
        return self.message_repository.get_recent_messages(
            receiver_id=receiver_id
        )

    @atomic
    def save_message(self, sender_id, receiver_id, content):

        message_model = self.chat_factory.create_private_chat(sender_id, receiver_id, content)
        user_friend_details = self.user_friend_repository.get_user_friend(message_model.sender_id, message_model.receiver_id)
        self.validator.validate_receiver_is_friend_or_not(user_friend_details=user_friend_details)
        self.validator.validate_send_message_eligibility(user_friend_details.get('status'))

        return self.message_repository.save_message(
            message_model.sender_id, 
            message_model.receiver_id, 
            message_model.content
        )

    @atomic
    def update_message(self, sender_id: int, reciever_id: int, message_id: int, content: str):
        message_model = self.chat_factory.update_private_chat(
            message_id=message_id,
            sender_id=sender_id, 
            receiver_id=reciever_id, 
            content=content
        )

        message_details = self.message_repository.get_message(message_id=message_model.id)
        self.validator.validate_message_existence(message_details=message_details)
        self.validator.validate_can_update_message(
            sender_id=message_model.sender_id, 
            existing_sender_id=message_details.get('sender_id')
        )
        self.message_repository.update_message(
            message_id=message_model.id, 
            sender_id=message_model.sender_id,
            receiver_id=message_model.receiver_id,
            content=message_model.content
        )

    @atomic
    def mark_message_as_seen(self, reciever_id: int, message_id: List[int]):
        self.message_repository.mark_message_as_seen(
            reciever_id=reciever_id, 
            message_ids=message_id
        )

    @atomic
    def delete_message(self, sender_id: int, message_id: int):
        message_details = self.message_repository.get_message(message_id=message_id)
        self.validator.validate_message_existence(message_details=message_details)
        self.validator.validate_can_delete_message(
            sender_id=sender_id, 
            existing_sender_id=message_details.get('sender_id')
        )
        self.message_repository.delete_message( sender_id=sender_id, message_id=message_id)