import abc
from typing import Optional, Dict, List

from django.contrib.auth import get_user_model
from django.db.models import Q

from user_management.user.domain import model as user_domain_model
from user_management.models import UserVerification

UserOrm = get_user_model()

class AbstractUserRepository(abc.ABC):


    @abc.abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id_object(self, user_id: int) -> Optional[object]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_users(user_filters: Dict = {}) -> List[Dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> Optional[Dict]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_email_or_username(self, email_or_username: str) -> Optional[object]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_user(self, user: user_domain_model.User, token: str) -> Dict:
        raise NotImplementedError

    @abc.abstractmethod
    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> Optional[Dict]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_password(self, user_id: int, password: str) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_is_active_by_id(self, email_or_username: str, is_active: bool) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_last_login(self, user_id: int, last_login) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError


class UserRepository(AbstractUserRepository):

    def create_user_to_dict(self, id, first_name, last_name, email, username):

        user_dict = {
            "id": id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username        
        }

        return user_dict

    def get_by_id(self, user_id: int) -> Optional[Dict]:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return

        return self.create_user_to_dict(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )
    
    def get_by_id_object(self, user_id: int) -> Optional[object]:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return

        return user_object

    def get_by_email(self, email: str) -> Optional[Dict]:
        try:
            user_object = UserOrm.objects.get(email=email)
        except UserOrm.DoesNotExist:
            return

        return self.create_user_to_dict(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )
    
    def get_by_username(self, username: str) -> Optional[Dict]:
        try:
            user_object = UserOrm.objects.get(username=username)
        except UserOrm.DoesNotExist:
            return

        return self.create_user_to_dict(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )

    def get_by_email_or_username(self, email_or_username: str) -> Optional[object]:
        user_object = UserOrm.objects.filter(Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)).first()
        return user_object

    def list_users(self, user_filters: Dict = None) -> List[Dict]:
        _q = Q()
        search_key = user_filters.get("search_key")
        if search_key:
            _q &= (
                Q(first_name__icontains=search_key) | 
                Q(last_name__icontains=search_key) | 
                Q(username__icontains=search_key)
            )

        queryset = (
            UserOrm.objects.filter(
                _q
            )
            .values(
                "id",
                "username",
                "first_name",
                "last_name",
            )
            .order_by(
                "first_name", 
                "last_name", 
                "username"
            )
        )

        return queryset

    def create_user(self, user: user_domain_model.User, token: str) -> Dict:
        user_object = UserOrm(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            username = user.username,
            is_active = user.is_active,
            is_staff = user.is_staff,
            is_superuser = user.is_superuser
        )
        user_object.set_password(user.password)
        user_object.save()
        UserVerification.objects.create(
            token = token,
            user_id = user_object.id
        )

        return self.create_user_to_dict(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username
        )

    def update_full_name(self, user_id: int, first_name: str, last_name: str) -> Optional[Dict]:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return
        
        user_object.first_name = first_name
        user_object.last_name = last_name
        user_object.save()

        return self.create_user_to_dict(
            id = user_object.id,
            first_name= user_object.first_name,
            last_name= user_object.last_name,
            email= user_object.email,
            username= user_object.username   
        )

    def update_password(self, user_id: int, password: str) -> None:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return
        
        user_object.set_password(password)
        user_object.save()

    def update_is_active_by_id(self, user_id: int, is_active: bool) -> None:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return

        user_object.is_active = is_active
        user_object.save()

    def update_last_login(self, user_id: int, last_login) -> None:
        UserOrm.objects.filter(id=user_id).update(last_login=last_login)

    def delete_user(self, user_id: int) -> bool:
        try:
            user_object = UserOrm.objects.get(id=user_id)
        except UserOrm.DoesNotExist:
            return False
        
        user_object.delete()

        return True