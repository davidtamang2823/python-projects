from abc import ABC, abstractmethod
from user_management.user.domain import model as user_domain_model

class AbstractUserFactory:


    @staticmethod
    @abstractmethod
    def create_user(
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str, 
        is_active: bool = False,
        is_superuser: bool = False,
        is_staff: bool = False, 
    ) -> user_domain_model.User:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_full_name(user_id: int, first_name: str, last_name: str) -> user_domain_model.User:
        raise NotImplementedError


class UserFactory(AbstractUserFactory):


    @staticmethod
    def create_user(
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str, 
        is_active: bool = False,
        is_superuser: bool = False,
        is_staff: bool = False, 
    ) -> user_domain_model.User:
        return user_domain_model.User(
            email = email,
            password = password,
            username = username,
            first_name = first_name,
            last_name = last_name,
            is_active = is_active,
            is_superuser = is_superuser,
            is_staff = is_staff
        )
    
    @staticmethod
    def update_full_name(user_id: int, first_name: str, last_name: str) -> user_domain_model.User:
        return user_domain_model.User(
            id = id,
            first_name = first_name,
            last_name = last_name
        )