from chat.message.domain import exceptions as domain_layer_exceptions
from chat.message.domain.model import PrivateChatModel
from abc import ABC, abstractmethod

class AbstractPrivateChatFactory(ABC):


    @abstractmethod
    def create_private_chat(self, sender_id: int, receiver_id: int, content: str) -> PrivateChatModel:
        raise NotImplementedError
    
    @abstractmethod
    def update_private_chat(self, message_id: int, sender_id: int, receiver_id: int, content: str) -> PrivateChatModel:
        raise NotImplementedError


class PrivateChatFactory(AbstractPrivateChatFactory):


    def create_private_chat(self, sender_id: int, receiver_id: int, content: str) -> PrivateChatModel:
        return PrivateChatModel(
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            content=content
        )

    def update_private_chat(self, message_id: int, sender_id: int, receiver_id: int, content: str) -> PrivateChatModel:
        return PrivateChatModel(
            id=message_id,
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            content=content
        )