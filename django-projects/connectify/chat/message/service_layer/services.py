from abc import ABC, abstractmethod
from chat.message.adapters.repository import AbstractPrivateMessageRepository
from chat.message.domain.factory import AbstractPrivateChatFactory
from chat.friend.adapters.repository import AbstractUserFriendRepository
from chat.message.service_layer.validator import PrivateChatValidator

class AbstractPrivateChatService(ABC):


    @abstractmethod
    def save_message(self, sender_id, receiver_id, content):
        pass

    @abstractmethod
    def get_chat_messages(self, user1_id, user2_id):
        pass



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

    def save_message(self, sender_id, receiver_id, content):

        message_model = self.chat_factory.create(sender_id, receiver_id, content)
        user_friend_details = self.user_friend_repository.get_user_friend(message_model.sender_id, message_model.receiver_id)
        self.validator.validate_receiver_is_friend_or_not(user_friend_details=user_friend_details)
        self.validator.validate_send_message_eligibility(user_friend_details.get('status'))

        self.message_repository.save_message(
            message_model.sender_id, 
            message_model.receiver_id, 
            message_model.content
        )

    def get_chat_messages(self, sender_id: int, receiver_id: int):
        return self.message_repository.get_messages_between_users(sender_id=sender_id, receiver_id=receiver_id)
