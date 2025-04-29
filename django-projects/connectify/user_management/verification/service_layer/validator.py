from typing import Dict
from django.utils import timezone
from datetime import datetime, timedelta
from user_management.verification.service_layer import exceptions as service_layer_exceptions


class CommonTokenValidator:


    def validate_token_is_expired(self, created_at: datetime):
        if (timezone.now() - created_at) > timedelta(minutes=15):
            raise service_layer_exceptions.TokenExpired
    
    def validate_token_is_none_or_not(self, token_details: Dict):
        if token_details is None:
            raise service_layer_exceptions.TokenNotFound

    def validate_resend_eligibility(self, created_at: datetime):
        if (timezone.now() - created_at) < timedelta(minutes=15):
            raise service_layer_exceptions.TokenNotExpired

class TokenValidator(CommonTokenValidator):


    def validate_user_registered_or_not(self, token_details: Dict):
        if token_details is None:
            raise service_layer_exceptions.UnregisteredUser
        
    def validate_user_is_verified_or_not(self, is_verified: bool):
        if is_verified is True:
            raise service_layer_exceptions.UserAlreadyVerified


class PasswordResetValidator(CommonTokenValidator):
    """Method Not Implemented"""