from typing import Optional, Dict
from abc import ABC, abstractmethod
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from user_management.models import UserVerification, PasswordResetVerification

UserOrm = get_user_model()

class AbstractTokenRepository(ABC):


    @abstractmethod
    def get_token(self, token: str):
        raise NotImplementedError

    @abstractmethod
    def store_token(self, token: str, user_id: int):
        raise NotImplementedError
    
    @abstractmethod
    def update_verification(self, token: str):
        raise NotImplementedError

    @abstractmethod
    def get_token_by_email_or_username(self, email_or_username: str) -> Optional[Dict]:
        raise NotImplementedError
    

class AbstractPasswordResetRepository(ABC):


    @abstractmethod
    def get_token(self, token: str) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    def get_token_by_email(self, email: str) -> Optional[Dict]:
        raise NotImplementedError
    
    @abstractmethod
    def store_token(self, token: str, user_id: int):
        raise NotImplementedError
    
    @abstractmethod
    def update_verfification(self, token: str):
        raise NotImplementedError


class TokenRepository(AbstractTokenRepository):


    def get_token(self, token: str) -> Optional[Dict]:
        try:
            token_obj = UserVerification.objects.get(token=token)
        except UserVerification.DoesNotExist:
            return
        
        return {
            'id': token_obj.id,
            'token': token_obj.token,
            'is_verified': token_obj.is_verified,
            'verified_at': token_obj.verified_at,
            'user_id': token_obj.user_id,
            'created_at': token_obj.created_at
        }
    

    def get_token_by_email_or_username(self, email_or_username: str) -> Optional[Dict]:
        token_obj = UserVerification.objects.filter(Q(user__email=email_or_username) | Q(user__username=email_or_username)).select_related('user').first()
        if token_obj is not None:
            return {
                'id': token_obj.id,
                'token': token_obj.token,
                'verfied_at': token_obj.verified_at,
                'is_verified': token_obj.is_verified,
                'user_id': token_obj.user_id,
                'created_at': token_obj.created_at,
                'email': token_obj.user.email,
                'username': token_obj.user.username
            }


    def store_token(self, token: str, user_id: int):
        UserVerification.objects.filter(user_id=user_id).delete()
        UserVerification.objects.create(
            token = token,
            user_id = user_id
        )

    def update_verification(self, token: str):
        try:
            token_obj = UserVerification.objects.get(token=token)
        except UserVerification.DoesNotExist:
            return
        
        token_obj.verified_at = timezone.now()
        token_obj.is_verified = True
        token_obj.user.is_active = True

        token_obj.user.save()
        token_obj.save()

        return {
            'id': token_obj.id,
            'token': token_obj.token,
            'verfied_at': token_obj.verified_at,
            'user_id': token_obj.user_id,
            'created_at': token_obj.created_at
        }
    

class PasswordResetRepository(AbstractPasswordResetRepository):


    def get_token(self, token: str) -> Optional[Dict]:
        try:
            password_reset_obj = PasswordResetVerification.objects.get(token=token)
        except PasswordResetVerification.DoesNotExist:
            return
        
        return {
            "reset_at" : password_reset_obj.reset_at,
            "created_at" : password_reset_obj.created_at,
            "token" : password_reset_obj.token,
            "user_id": password_reset_obj.user_id
        }

    def get_token_by_email(self, email: str) -> Optional[Dict]:
        try:
            password_reset_obj = PasswordResetVerification.objects.get(user__email=email)
        except PasswordResetVerification.DoesNotExist:
            return

        return {
            "reset_at" : password_reset_obj.reset_at,
            "created_at" : password_reset_obj.created_at,
            "token" : password_reset_obj.token,
            "user_id": password_reset_obj.user_id
        }
        
    def store_token(self, token: str, user_id: int):
        PasswordResetVerification.objects.filter(
            user_id = user_id
        ).delete()
        PasswordResetVerification.objects.create(
            token = token,
            user_id = user_id
        )


    def update_verfification(self, token: str):
        try:
            password_reset_obj = PasswordResetVerification.objects.get(token=token)
        except PasswordResetVerification.DoesNotExist:
            return

        password_reset_obj.reset_at = timezone.now()
        password_reset_obj.save()