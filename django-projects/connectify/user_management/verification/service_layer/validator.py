from typing import Dict
from datetime import datetime, timedelta
from user_management.verification.service_layer import exceptions as service_layer_exceptions


class TokenValidator:


    def validate_token_is_expired(self, created_at: datetime):
        if (datetime.now() - created_at) > timedelta(minutes=15):
            raise service_layer_exceptions.TokenExpired
    
    def validate_token_is_none_or_not(self, token_details: Dict):
        if token_details is None:
            raise service_layer_exceptions.TokenNotFound
        
    def validate_user_is_active_or_not(self, verified_at: datetime):
        if verified_at is not None:
            raise service_layer_exceptions.UserAlreadyVerified

    def validate_resend_eligibility(self, created_at: datetime):
        if (datetime.now() - created_at) < timedelta(minutes=15):
            raise service_layer_exceptions.TokenNotExpired

    def validate_user_registered_or_not(self, token_details: Dict):
        if token_details is None:
            raise service_layer_exceptions.UnregisteredUser