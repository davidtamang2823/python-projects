import random
from abc import ABC, abstractmethod
from user_management.user.domain import model as user_domain_model
from user_management.user.domain import events as user_events
from user_management.user.common import constants as user_constants

class AbstractUserFactory(ABC):


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
            is_staff = is_staff,
            events = [
                user_events.SendUserRegistrationConfirmationEmail(
                    event_type=user_constants.USER_REGISTRATION,
                    source=user_constants.EVENT_SOURCE,
                    send_to=email,
                    verification_code=random.randint(100000, 999999),
                )
            ]
        )
    
    @staticmethod
    def update_full_name(user_id: int, first_name: str, last_name: str) -> user_domain_model.User:
        return user_domain_model.User(
            id = user_id,
            first_name = first_name,
            last_name = last_name
        )