from typing import Dict
from abc import ABC, abstractmethod
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from chat.models import UserFriend


class AbstractUserFriendRepository(ABC):


    @abstractmethod
    def get_user_friend(self, user_id, friend_id):
        raise NotImplementedError
    
    @abstractmethod
    def get_user_friends(self, user_id: int, list_filter: Dict):
        raise NotImplementedError
    
    @abstractmethod
    def get_friend_requests(self, user_id: int, list_filter: Dict):
        raise NotImplementedError

    @abstractmethod
    def save_friend_request(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError
    
    @abstractmethod
    def update_user_friend(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError
    
    @abstractmethod
    def remove_friend(self, user_id: int, friend_id: int):
        raise NotImplementedError
    

class UserFriendRepository(AbstractUserFriendRepository):


    def get_user_friend(self, user_id: int, friend_id: int):
        try:
            user_friend_object = UserFriend.objects.get(user_id=user_id, friend_id=friend_id)
        except UserFriend.DoesNotExist:
            return 
        
        return {
            'status': user_friend_object.status
        }

    def get_queryset(self, filter_object):
        user_friends = UserFriend.objects.filter(
            filter_object        
        ).annotate(
            first_name = F('friend__first_name'),
            last_name = F('friend__last_name'),
            username = F('friend__username')
        ).values(
            'friend_id',
            'first_name',
            'last_name',
            'username',
            'status'
        ).order_by(
            'first_name',
            'last_name',
        )

        return user_friends

    def get_user_friends(self, user_id: int, list_filter: Dict):
        search_key = list_filter.get('search_key')
        filter_object = Q(user_id=user_id)
        if search_key:
            filter_object &= Q(first_name__icontains=search_key) | Q(last_name__icontains=search_key) |  Q(username__istartswith=search_key)

        return self.get_queryset(filter_object=filter_object)


    def get_friend_requests(self, user_id: int, list_filter: Dict):
        search_key = list_filter.get('search_key')
        filter_object = Q(friend_id=user_id) & Q(status='pending')
        if search_key:
            filter_object &= Q(first_name__icontains=search_key) | Q(last_name__icontains=search_key) |  Q(username__istartswith=search_key)
        friend_requests = self.get_queryset(
            filter_object=filter_object
        )
        return friend_requests

    def save_friend_request(self, user_id: int, friend_id: int, status: str):
        UserFriend.objects.bulk_create(
            [
                UserFriend(
                    user_id = user_id,
                    friend_id = friend_id,
                    status = status
                )
            ]
        )

    def update_user_friend(self, user_id: int, friend_id: int, status: str):
        UserFriend.objects.filter(
            user_id=user_id, 
            friend_id=friend_id
        ).update(status=status)


    def remove_friend(self, user_id: int, friend_id: int):
        UserFriend.objects.filter(
            user_id = user_id,
            friend_id = friend_id
        ).delete()