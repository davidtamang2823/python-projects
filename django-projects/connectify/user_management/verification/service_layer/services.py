from secrets import token_urlsafe
from abc import ABC, abstractmethod
from django.db.transaction import atomic
from events import message_bus
from user_management.verification.adapters.repository import AbstractTokenRepository
from user_management.verification.service_layer.validator import TokenValidator
from user_management.verification.domain.factory import AbstractUserVerificationFactory
class AbstractTokenService(ABC):

    
    @abstractmethod
    def verify_token(self, token: str):
        raise NotImplementedError

    @abstractmethod
    def resend_verification_email(self, email_or_username: str):
        raise NotImplementedError

    

class TokenService(AbstractTokenService):


    def __init__(self, repository: AbstractTokenRepository, factory: AbstractUserVerificationFactory, validator: TokenValidator):
        self.repository = repository
        self.validator = validator
        self.factory = factory

    @atomic
    def verify_token(self, token: str):
        token_details = self.repository.get_token(token=token)
        self.validator.validate_token_is_none_or_not(token_details=token_details)
        self.validator.validate_token_is_expired(created_at=token_details.get('created_at'))
        self.repository.update_verification(token=token)

    @atomic
    def resend_verification_email(self, email_or_username: str):
        token_details = self.repository.get_token_by_email_or_username(email_or_username=email_or_username)
        self.validator.validate_user_registered_or_not(token_details=token_details)
        self.validator.validate_user_is_active_or_not(verified_at=token_details.get('verified_at'))
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