from django.db import models
from django.conf import settings

class PrivateMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='received_messages')
    content = models.TextField(max_length=20000, min_length=1)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        default_permissions = ()

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.created_at}"