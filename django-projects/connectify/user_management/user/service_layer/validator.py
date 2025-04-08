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

    def validate_user_not_none(self, user_object):
        if user_object is None:
            raise user_service_layer_exceptions.UserNotFound

    def validate_user_exists_by_id(self, user_id):
        if self.repository.get_by_id(user_id=user_id) is None:
            raise user_service_layer_exceptions.UserNotFound