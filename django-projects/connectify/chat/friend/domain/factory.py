from abc import ABC, abstractmethod
from chat.friend.domain import model as user_friend_domain_model

class AbstractUserFriendFactory(ABC):


    @abstractmethod
    def create_user_friend(
        self,
        user_id: int,
        friend_id: int,
    ) -> user_friend_domain_model.UserFriend:
        raise NotImplementedError
    
    @abstractmethod
    def update_user_friend(
        self,
        user_id: int,
        friend_id: int,
        status: str
    ) -> user_friend_domain_model.UserFriend:
        raise NotImplementedError
    
    @abstractmethod
    def delete_user_friend(self, user_id: int, friend_id: int) -> user_friend_domain_model.UserFriend:
        raise NotImplementedError


class UserFriendFactory(AbstractUserFriendFactory):


    def create_user_friend(
        self,
        user_id: int,
        friend_id: int,
    ) -> user_friend_domain_model.UserFriend:
        return user_friend_domain_model.UserFriend(
            user_id = user_id,
            friend_id = friend_id
        )
    
    def update_user_friend(
        self,
        user_id: int,
        friend_id: int,
        status: str
    ) -> user_friend_domain_model.UserFriend:
        return user_friend_domain_model.UserFriend(
            user_id = user_id,
            friend_id = friend_id,
            status = status
        )
    
    def delete_user_friend(
        self,
        user_id: int, 
        friend_id: int
    ) -> user_friend_domain_model.UserFriend:
        return user_friend_domain_model.UserFriend(
            user_id = user_id,
            friend_id = friend_id
        )
