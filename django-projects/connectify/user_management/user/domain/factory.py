from abc import ABC, abstractmethod
from user_management.user.domain import model as user_domain_model
from user_management.user.domain import events as user_events
from user_management.user.common import constants as user_constants

class AbstractUserFactory(ABC):


    @abstractmethod
    def create_user(
        self,
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str, 
        token: str,
        is_active: bool = False,
        is_superuser: bool = False,
        is_staff: bool = False, 
    ) -> user_domain_model.User:
        raise NotImplementedError
    
    @abstractmethod
    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> user_domain_model.User:
        raise NotImplementedError


class UserFactory(AbstractUserFactory):


    def create_user(
        self,
        email: str, 
        password: str, 
        username: str, 
        first_name: str, 
        last_name: str,
        token: str,
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
                user_events.SendUserVerificationEmail(
                    event_type=user_constants.USER_REGISTRATION,
                    source=user_constants.EVENT_SOURCE,
                    send_to=email,
                    send_to_username=username,
                    verification_token=token,
                )
            ]
        )
    
    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> user_domain_model.User:
        return user_domain_model.User(
            id = user_id,
            first_name = first_name,
            last_name = last_name
        )