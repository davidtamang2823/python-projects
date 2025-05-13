from abc import ABC, abstractmethod
from django.db.models import Q, F, OuterRef, Subquery
from chat.models import PrivateMessage


class AbstractPrivateMessageRepository(ABC):


    @abstractmethod
    def get_messages_between_users(self, sender_id: int, receiver_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_recent_messages(self, receiver_id: int):
        raise NotImplementedError

    @abstractmethod
    def save_message(self, sender_id: int, receiver_id: int, content: str):
        raise NotImplementedError



class PrivateMessageRepository(AbstractPrivateMessageRepository):


    def get_messages_between_users(self, sender_id: int, receiver_id: int):
        return PrivateMessage.objects.filter(
            (Q(sender_id=sender_id) & Q(receiver=receiver_id)) | 
            (Q(sender=receiver_id) & Q(receiver=sender_id))
        ).order_by(
            'created_at'
        ).values(
            'id',
            'sender_id', 
            'receiver_id',
            'content', 
            'created_at',
            'is_seen'
        )


    def get_recent_messages(self, receiver_id: int):
        unseen_messages_count = PrivateMessage.objects.filter(
            receiver_id=receiver_id,
            sender_id=OuterRef('sender_id'),
            is_seen=False
        ).count()

        return PrivateMessage.objects.filter(
            receiver_id = receiver_id,
            is_seen = False
        ).annotate(
            unseen_count=Subquery(unseen_messages_count)
        ).order_by(
            '-created_at'
        ).distinct(
            'sender_id'
        ).values(
            'id',
            'sender_id', 
            'receiver_id',
            'content', 
            'created_at',
            'is_seen'
        )


    def save_message(self, sender_id: int, receiver_id: int, content: str):

        PrivateMessage.objects.create(
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            content=content
        )

    
