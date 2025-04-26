from http import HTTPMethod
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from user_management.verification.service_layer.services import TokenService 
from user_management.verification.adapters.repository import TokenRepository
from user_management.verification.service_layer.validator import TokenValidator
from user_management.verification.domain.factory import UserVerificationFactory

class VerificationViewSet(ViewSet):

    @property
    def service(self) -> TokenService:
        return TokenService(
            repository=TokenRepository(),
            validator=TokenValidator(),
            factory=UserVerificationFactory()
        )

    @action(detail=False, methods=[HTTPMethod.GET])
    def resend_verification_email(self, request):
        self.service.resend_verification_email(
            email_or_username = request.data.get('email_or_username')
        )

    @action(detail=False, methods=[HTTPMethod.PATCH])
    def verify(self, request):
        self.service.verify_token(
            token = request.data.get('token')
        )