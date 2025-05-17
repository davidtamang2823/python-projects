from abc import ABC, abstractmethod
from typing import List
from django.db.models import Q, F, OuterRef, Subquery, Case, When, TextField
from chat.models import PrivateMessage


class AbstractPrivateMessageRepository(ABC):


    @abstractmethod
    def get_message(self, message_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_messages_between_users(self, sender_id: int, receiver_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_recent_messages(self, receiver_id: int):
        raise NotImplementedError

    @abstractmethod
    def save_message(self, sender_id: int, receiver_id: int, content: str):
        raise NotImplementedError

    @abstractmethod
    def update_message(self, message_id: int, sender_id: int, receiver_id: int, content: str):
        raise NotImplementedError

    @abstractmethod
    def mark_message_as_seen(self, receiver_id: int, message_ids: List[int]):
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, sender_id: int, message_id: int):
        raise NotImplementedError

class PrivateMessageRepository(AbstractPrivateMessageRepository):


    def get_message(self, message_id: int):
        return PrivateMessage.objects.filter(
            id=message_id
        ).values(
            'id',
            'sender_id', 
            'receiver_id',
            'content', 
            'created_at',
            'updated_at',
            'is_seen'
        ).first()

    def get_messages_between_users(self, sender_id: int, receiver_id: int):
        return PrivateMessage.objects.filter(
            (Q(sender_id=sender_id) & Q(receiver=receiver_id)) | 
            (Q(sender=receiver_id) & Q(receiver=sender_id))
        ).annotate(
            content = Case(
                When(is_deleted=True, then='This message has been deleted'),
                default=F('content'),
                output_field=TextField()
            )
        ).order_by(
            'created_at'
        ).values(
            'id',
            'sender_id', 
            'receiver_id',
            'content', 
            'created_at',
            'updated_at',
            'is_seen'
        )

    def get_recent_messages(self, receiver_id: int):
        unseen_messages_count = PrivateMessage.objects.filter(
            receiver_id=receiver_id,
            sender_id=OuterRef('sender_id'),
            is_seen=False,
            is_deleted=False
        ).count()

        return PrivateMessage.objects.filter(
            receiver_id = receiver_id,
            is_seen = False,
            is_deleted = False
        ).annotate(
            unseen_count=Subquery(unseen_messages_count),
            sender_first_name=F('sender__first_name'),
            sender_last_name=F('sender__last_name'),
        ).order_by(
            '-created_at'
        ).distinct(
            'sender_id'
        ).values(
            'sender_id',
            'sender_first_name',
            'sender_last_name',
            'receiver_id',
            'unseen_count',
            'content', 
            'updated_at',
            'created_at',
        )

    def save_message(self, sender_id: int, receiver_id: int, content: str):
        private_message = PrivateMessage.objects.create(
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            content=content
        )
        return {
            'id': private_message.id,
            'sender_id': private_message.sender_id,
            'receiver_id': private_message.receiver_id,
            'content': private_message.content,
            'created_at': private_message.created_at,
            'updated_at': private_message.updated_at,
            'is_seen': private_message.is_seen
        }

    def update_message(self, message_id: int, sender_id: int, receiver_id: int, content: str):
        PrivateMessage.objects.filter(
            id=message_id,
            sender_id=sender_id,
            receiver_id=receiver_id
        ).update(
            content=content
        )

    def mark_message_as_seen(self, receiver_id: int, message_ids: List[int]):
        PrivateMessage.objects.filter(
            receiver_id=receiver_id,
            id__in=message_ids
        ).update(
            is_seen=True
        )


    def delete_message(self, sender_id: int, message_id: int):
        PrivateMessage.objects.filter(
            id=message_id,
            sender_id=sender_id
        ).update(
            is_deleted=True
        )