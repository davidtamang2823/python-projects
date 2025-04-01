from user_management.user.adapters.repository import AbstractUserRepository
from user_management.user.service_layer import exceptions as user_service_layer_exceptions

class UserValidator:

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def validate_email_uniqueness(self, email):
        if self.repository.get_by_email(email=email) is not None:
            raise user_service_layer_exceptions.EmailAlreadyExists

    def validate_username_uniquness(self, username):
        if self.repository.get_by_username(username=username) is not None:
            raise user_service_layer_exceptions.UserNameAlreadyExists