from django.contrib.auth.backends import ModelBackend
from user_management.user.adapters.repository import UserRepository
from user_management.authentication.jwt.service_layer.services import JwtAuthService
from user_management.authentication.jwt.domain.factory import AuthenticationFactory

jwt_service = JwtAuthService(
    user_repository=UserRepository(),
    factory=AuthenticationFactory()
)

class EmailOrUsernameBackend(ModelBackend):


    def authenticate(
        self,
        request,
        username,
        password,
        **kwargs
    ):
        user = jwt_service.authenticate(email_or_username=username, password=password)
        return user