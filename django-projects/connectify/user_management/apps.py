import importlib
from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'

    def ready(self):
        importlib.import_module("user_management.user.service_layer.event_handlers")
        importlib.import_module("user_management.verification.service_layer.event_handlers")