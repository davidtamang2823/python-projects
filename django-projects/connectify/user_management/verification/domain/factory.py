from abc import ABC, abstractmethod
from user_management.verification.domain import model as verification_domain_model
from user_management.verification.domain import events as verfication_events
from user_management.verification.common import constants

class AbstractUserVerificationFactory(ABC):


    @abstractmethod
    def create_user_verification(
        self,
        token: str,
        send_to: str,
        send_to_username: str
    ) -> verification_domain_model.UserVerification:
        raise NotImplementedError
    

class AbstractPasswordResetFactory(ABC):

    @abstractmethod
    def create_password_reset(self, email: str, token: str, send_to_username: str) -> verification_domain_model.PasswordReset:
        raise NotImplementedError

    @abstractmethod
    def update_password_reset(self, password: str, token: str) -> verification_domain_model.PasswordReset:
        raise NotImplementedError

class UserVerificationFactory(AbstractUserVerificationFactory):


    def create_user_verification(
        self,
        token: str,
        send_to: str,
        send_to_username: str
    ) -> verification_domain_model.UserVerification:
        
        return verification_domain_model.UserVerification(
            token = token,
            events = [
                verfication_events.ResendUserVerificationEmail(
                    verification_token = token,
                    send_to_username = send_to_username,
                    send_to = send_to,
                    event_type = constants.RESEND_VERIFICATION_EMAIL,
                    source = constants.EVENT_SOURCE
                )
            ]
        )
    

class PasswordResetFactory(AbstractPasswordResetFactory):


    def create_password_reset(self, email: str, token: str, send_to_username: str) -> verification_domain_model.PasswordReset:
        return verification_domain_model.PasswordReset(
            token = token,
            email = email,
            events = [
                verfication_events.SendPasswordResetEmail(
                    verification_token = token,
                    send_to_username = send_to_username,
                    send_to = email,
                    event_type = constants.SEND_PASSWORD_RESET_EMAIL,
                    source = constants.EVENT_SOURCE
                )
            ]
        )

    def update_password_reset(self, password: str, token: str) -> verification_domain_model.PasswordReset:
        return verification_domain_model.PasswordReset(
            token = token,
            password = password
        )