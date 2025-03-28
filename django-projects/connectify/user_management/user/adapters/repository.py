import abc
from typing import Optional
from user_management.user.domain import model as user_domain_model
from django.contrib.auth import get_user_model

UserOrm = get_user_model()

class AbstractUserRepository(abc.ABC):


    @abc.abstractmethod
    def get_by_id(self, user_id: int) -> Optional[user_domain_model.User]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[user_domain_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_user(self, user: user_domain_model.User) -> user_domain_model.User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> Optional[user_domain_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError


class UserRepository(AbstractUserRepository):

    def create_user_to_domain_model(self, id, first_name, last_name, email, username):

        user = user_domain_model.User(
            id = id,
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
        )

        return user

    def get_by_id(self, user_id: int) -> Optional[user_domain_model.User]:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return

        user = self.create_user_to_domain_model(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )

        return user

    def get_by_email(self, email: str) -> Optional[user_domain_model.User]:
        try:
            user_object = UserOrm.objects.get(email=email)
        except UserOrm.DoesNotExist:
            return

        user = self.create_user_to_domain_model(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )

        return user

    def create_user(self, user: user_domain_model.User) -> user_domain_model.User:
        user_object = UserOrm.objects.create(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            username = user.username,
            password = user.password,
            is_active = user.is_active,
            is_staff = user.is_staff,
            is_superuser = user.is_superuser
        )

        user = self.create_user_to_domain_model(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )

        return user


    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> Optional[user_domain_model.User]:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return
        
        user_object.first_name = first_name
        user_object.last_name = last_name
        user_object.save()

        user = self.create_user_to_domain_model(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username        
        )

        return user

    def delete_user(self, user_id: int) -> bool:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return False
        
        user_object.delete()

        return True