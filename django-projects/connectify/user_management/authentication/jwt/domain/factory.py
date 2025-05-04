from abc import ABC, abstractmethod
from user_management.authentication.jwt.domain import model as authentication_domain_model

class AbstractAuthenticationFactory(ABC):


    @abstractmethod
    def create_authentication(
        self,
        email_or_username: str,
        password: str 
    ) -> authentication_domain_model.Authentication:
        raise NotImplementedError



class AuthenticationFactory(AbstractAuthenticationFactory):


    def create_authentication(
        self,
        email_or_username: str,
        password: str 
    ) -> authentication_domain_model.Authentication:
        return authentication_domain_model.Authentication(
            email_or_username=email_or_username,
            password=password
        )