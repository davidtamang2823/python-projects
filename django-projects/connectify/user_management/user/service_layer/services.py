from abc import ABC, abstractmethod
from user_management.user.domain.factory import AbstractUserFactory
from user_management.user.adapters.repository import AbstractUserRepository

class AbstractUserService(ABC):


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



class UserService(AbstractUserService):


    def __init__(self, repository: AbstractUserRepository, factory: AbstractUserFactory):
        self.repository = repository
        self.factory = factory

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
    ) -> None:
        
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

        self.repository.create_user(user=user)
    
    @abstractmethod
    def update_full_name(
        self,
        user_id: int,
        first_name: str,
        last_name: str
    ) -> None:
        
        user = self.factory.update_full_name(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name
        )

        self.repository.update_full_name(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name
        )

