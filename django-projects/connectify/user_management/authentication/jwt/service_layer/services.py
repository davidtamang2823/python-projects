from abc import ABC, abstractmethod

from django.utils import timezone

from user_management.user.adapters.repository import AbstractUserRepository
from user_management.authentication.jwt.domain.factory import AbstractAuthenticationFactory


class AbstractJwtAuthService(ABC):


    @abstractmethod
    def authenticate(self, email_or_username: str, password: str):
        raise NotImplementedError
    


class JwtAuthService(AbstractJwtAuthService):


    def __init__(self, user_repository: AbstractUserRepository, factory: AbstractAuthenticationFactory):
        self.user_repository = user_repository
        self.factory = factory

    def authenticate(self, email_or_username: str, password: str):
        try:
            authentication_model = self.factory.create_authentication(email_or_username=email_or_username, password=password)
        except Exception:
            return
        else:
            user_orm_object = self.user_repository.get_by_email_or_username(email_or_username=authentication_model.email_or_username)
            if user_orm_object and user_orm_object.check_password(authentication_model.password):
                self.user_repository.update_last_login(user_orm_object.id, timezone.now())
                return user_orm_object
