from secrets import token_urlsafe
from abc import ABC, abstractmethod
from django.db.transaction import atomic
from events import message_bus
from user_management.verification.adapters.repository import AbstractTokenRepository, AbstractPasswordResetRepository
from user_management.verification.service_layer.validator import TokenValidator, PasswordResetValidator
from user_management.verification.domain.factory import AbstractUserVerificationFactory, AbstractPasswordResetFactory
from user_management.user.adapters.repository import AbstractUserRepository
class AbstractTokenService(ABC):

    
    @abstractmethod
    def verify_token(self, token: str):
        raise NotImplementedError

    @abstractmethod
    def resend_verification_email(self, email_or_username: str):
        raise NotImplementedError

class AbstractPasswordResetService(ABC):


    @abstractmethod
    def send_password_reset_email(self, email: str):
        raise NotImplementedError
    
    @abstractmethod
    def verify_token_and_update_password(self, token: str, password: str):
        raise NotImplementedError
    

class TokenService(AbstractTokenService):


    def __init__(
        self, 
        repository: AbstractTokenRepository, 
        factory: AbstractUserVerificationFactory, 
        validator: TokenValidator
    ):
        self.repository = repository
        self.validator = validator
        self.factory = factory

    @atomic
    def verify_token(self, token: str):
        token_details = self.repository.get_token(token=token)
        self.validator.validate_token_is_none_or_not(token_details=token_details)
        self.validator.validate_token_is_expired(created_at=token_details.get('created_at'))
        self.validator.validate_user_is_verified_or_not(is_verified=token_details.get('is_verified'))
        self.repository.update_verification(token=token)

    @atomic
    def resend_verification_email(self, email_or_username: str):
        token_details = self.repository.get_token_by_email_or_username(email_or_username=email_or_username)
        self.validator.validate_user_registered_or_not(token_details=token_details)
        self.validator.validate_user_is_verified_or_not(is_verified=token_details.get('is_verified'))
        self.validator.validate_resend_eligibility(created_at=token_details.get('created_at'))

        token = token_urlsafe(48)
        
        user_verification_model = self.factory.create_user_verification(
            token=token,
            send_to=token_details.get('email'),
            send_to_username=token_details.get('username')
        )

        self.repository.store_token(
            token=user_verification_model.token, 
            user_id=token_details.get('user_id')
        )

        message_bus.dispatch_events(user_verification_model.events)


class PasswordResetService(AbstractPasswordResetService):


    def __init__(
        self, 
        password_reset_repository: AbstractPasswordResetRepository, 
        user_repository: AbstractUserRepository,
        factory: AbstractPasswordResetFactory, 
        validator: PasswordResetValidator
    ):
        self.password_reset_repository = password_reset_repository
        self.user_repository = user_repository
        self.validator = validator
        self.factory = factory

    @atomic
    def send_password_reset_email(self, email: str):
        user_details = self.user_repository.get_by_email(email=email)
        if user_details:
            token_details = self.password_reset_repository.get_token_by_email(email=email)
            if token_details and token_details.get('reset_at') is None:
                self.validator.validate_resend_eligibility(created_at=token_details.get('created_at'))
            token = token_urlsafe(48)
            password_reset_model = self.factory.create_password_reset(
                email = email,
                token = token,
                send_to_username= user_details.get('username')
            )
            self.password_reset_repository.store_token(
                token=password_reset_model.token,
                user_id=user_details.get('id')
            )
            message_bus.dispatch_events(password_reset_model.events)

    @atomic
    def verify_token_and_update_password(self, token: str, password: str):
        token_details = self.password_reset_repository.get_token(token=token)
        self.validator.validate_token_is_none_or_not(token_details=token_details)
        self.validator.validate_token_is_expired(created_at=token_details.get('created_at'))
        password_reset_model = self.factory.update_password_reset(password=password, token=token)
        self.password_reset_repository.update_verfification(password_reset_model.token)
        self.user_repository.update_password(
            user_id=token_details.get('user_id'),
            password=password
        )