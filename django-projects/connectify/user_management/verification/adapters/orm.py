from django.db import models
from django.conf import settings

class UserVerification(models.Model):


    verified_at = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification')

    class Meta:
        default_permissions = ()


class PasswordResetVerification(models.Model):


    reset_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='password_reset')