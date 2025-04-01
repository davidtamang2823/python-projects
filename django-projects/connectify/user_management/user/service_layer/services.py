from abc import ABC, abstractmethod
from typing import List, Dict

from django.db.transaction import atomic

from events import MessageBus
from user_management.user.domain.factory import AbstractUserFactory
from user_management.user.adapters.repository import AbstractUserRepository
from user_management.user.service_layer.validator import UserValidator
class AbstractUserService(ABC):


    @abstractmethod
    def list_users(self, user_filters: Dict):
        raise NotImplementedError
    
    @abstractmethod
    def get_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def register_user(
        self,
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str, 
        is_active: bool = False,
        is_superuser: bool = False,
        is_staff: bool = False,        
    ):
        raise NotImplementedError
    
    @abstractmethod
    def update_full_name(
        self,
        user_id: int,
        first_name: str,
        last_name: str
    ):
        raise NotImplementedError

    @abstractmethod
    def delete_user(
        self,
        user_id: int
    ):
        raise NotImplementedError



class UserService(AbstractUserService):


    def __init__(
        self, 
        repository: AbstractUserRepository, 
        factory: AbstractUserFactory, 
        message_bus: MessageBus,
        validator: UserValidator,
    ):
        self.repository = repository
        self.factory = factory
        self.message_bus = message_bus
        self.validator = validator

    def list_users(self, user_filters: dict) -> List[Dict]:
        return self.repository.list_users(user_filters=user_filters)

    def get_user(self, user_id: int) -> Dict:
        return self.repository.get_by_id(user_id=user_id)

    @atomic
    def register_user(
        self,
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str, 
        is_active: bool = False,
        is_superuser: bool = False,
        is_staff: bool = False,             
    ) -> Dict:
        
        self.validator.validate_email_uniqueness(email=email)
        self.validator.validate_username_uniquness(username=username)

        user = self.factory.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_superuser=is_superuser,
            is_staff=is_staff
        )

        self.message_bus.dispatch_events(user.events)

        return self.repository.create_user(user=user)
    
    @atomic
    def update_full_name(
        self,
        user_id: int,
        first_name: str,
        last_name: str
    ) -> Dict:
        
        user = self.factory.update_full_name(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name
        )

        return self.repository.update_full_name(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name
        )

    @atomic
    def delete_user(self, user_id: int) -> None:
        self.repository.delete_user(user_id=user_id)
