from typing import Dict
from abc import ABC, abstractmethod
from django.db.transaction import atomic
from chat.friend.domain.factory import AbstractUserFriendFactory
from chat.friend.adapters.repository import AbstractUserFriendRepository
from chat.friend.service_layer.validator import UserFriendValidator

class AbstractUserFriendService(ABC):

    @abstractmethod
    def get_friends_list(self, user_id: int, list_filter: Dict):
        raise NotImplementedError
    
    @abstractmethod
    def get_friend_requests(self, user_id: int, list_filter: Dict):
        raise NotImplementedError

    @abstractmethod
    def send_friend_request(self, user_id: int, friend_id: int):
        raise NotImplementedError

    @abstractmethod
    def accept_friend_request(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError
    
    @abstractmethod
    def reject_friend_request(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError

    @abstractmethod
    def block_friend(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError

    @abstractmethod
    def remove_friend(self, user_id: int, friend_id: int):
        raise NotImplementedError

    @abstractmethod
    def unblock_friend(self, user_id: int, friend_id: int, status: str):
        raise NotImplementedError


class UserFriendService(AbstractUserFriendService):


    def __init__(self, repository: AbstractUserFriendRepository, factory: AbstractUserFriendFactory, validator: UserFriendValidator):
        self.repository = repository
        self.factory = factory
        self.validator = validator

    def get_friends_list(self, user_id: int, list_filter: Dict):
        return self.repository.get_user_friends(user_id=user_id, list_filter=list_filter)


    def get_friend_requests(self, user_id: int, list_filter: Dict):
        return self.repository.get_friend_requests(user_id=user_id, list_filter=list_filter)

    @atomic
    def send_friend_request(self, user_id: int, friend_id: int):

        user_friend_model = self.factory.create_user_friend(
            user_id=user_id,
            friend_id=friend_id
        )

        user_friend_details = self.repository.get_user_friend(
            user_id=user_friend_model.user_id,
            friend_id=user_friend_model.friend_id,
        )

        if user_friend_details:
            self.validator.validate_can_send_request(current_status=user_friend_details.get('status'))

        if user_friend_details.get('status') == 'rejected':
            self.repository.remove_friend(
                user_id=user_friend_model.user_id, 
                friend_id=user_friend_model.friend_id
            )

        self.repository.save_friend_request(
            user_id=user_friend_model.user_id,
            friend_id=user_friend_model.friend_id,
            status=user_friend_model.status.value 
        )


    @atomic
    def accept_friend_request(self, user_id: int, friend_id: int, status: str):
        user_friend_model = self.factory.update_user_friend(
            user_id=user_id,
            friend_id=friend_id,
            status=status
        )

        user_friend_details = self.repository.get_user_friend(
            user_id=user_friend_model.friend_id,
            friend_id=user_friend_model.user_id,
        )

        self.validator.validate_friend_exists_or_not(user_friend_details=user_friend_details)

        if user_friend_details.get('status') == 'pending' and user_friend_model.status.value == 'accepted':
            self.repository.save_friend_request(
                user_id = user_friend_model.user_id,
                friend_id = user_friend_model.friend_id,
                status = user_friend_model.status.value
            )

            self.repository.update_user_friend(
                user_id=user_friend_model.friend_id,
                friend_id=user_friend_model.user_id,
                status=user_friend_model.status.value
            )

    @atomic
    def reject_friend_request(self, user_id: int, friend_id: int, status: str):
        user_friend_model = self.factory.update_user_friend(
            user_id=user_id,
            friend_id=friend_id,
            status=status
        )

        user_friend_details = self.repository.get_user_friend(
            user_id=user_friend_model.friend_id,
            friend_id=user_friend_model.user_id,
        )

        self.validator.validate_friend_exists_or_not(user_friend_details=user_friend_details)

        if user_friend_details.get('status') == 'pending' and user_friend_model.status.value == 'rejected':
            self.repository.update_user_friend(
                user_id=user_friend_model.user_id,
                friend_id=user_friend_model.friend_id,
                status=user_friend_model.status.value
            )

    @atomic
    def block_friend(self, user_id: int, friend_id: int, status: str):
        user_friend_model = self.factory.update_user_friend(
            user_id=user_id,
            friend_id=friend_id,
            status=status
        )

        user_friend_details = self.repository.get_user_friend(
            user_id=user_friend_model.user_id,
            friend_id=user_friend_model.friend_id,
        )

        self.validator.validate_friend_exists_or_not(user_friend_details=user_friend_details)

        if user_friend_details.get('status') == 'accepted' and user_friend_model.status.value == 'blocked':
            self.repository.update_user_friend(
                user_id=user_friend_model.user_id,
                friend_id=user_friend_model.friend_id,
                status=user_friend_model.status.value
            )

    @atomic
    def unblock_friend(self, user_id: int, friend_id: int, status: str):
        user_friend_model = self.factory.update_user_friend(
            user_id=user_id,
            friend_id=friend_id,
            status=status
        )

        user_friend_details = self.repository.get_user_friend(
            user_id=user_friend_model.user_id,
            friend_id=user_friend_model.friend_id,
        )

        self.validator.validate_friend_exists_or_not(user_friend_details=user_friend_details)

        if user_friend_details.get('status') == 'blocked' and user_friend_model.status.value == 'accepted':
            self.repository.update_user_friend(
                user_id=user_friend_model.user_id,
                friend_id=user_friend_model.friend_id,
                status=user_friend_model.status.value
            )

    @atomic
    def remove_friend(self, user_id: int, friend_id: int):
        user_friend_model = self.factory.delete_user_friend(
            user_id=user_id,
            friend_id=friend_id
        )
        self.repository.remove_friend(
            user_id=user_friend_model.user_id, 
            friend_id=user_friend_model.friend_id
        )
        self.repository.remove_friend(
            user_id=user_friend_model.friend_id, 
            friend_id=user_friend_model.user_id
        )