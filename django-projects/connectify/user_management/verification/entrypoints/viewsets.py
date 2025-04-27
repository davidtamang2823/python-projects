from http import HTTPMethod
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from user_management.verification.service_layer.services import TokenService 
from user_management.verification.adapters.repository import TokenRepository
from user_management.verification.service_layer.validator import TokenValidator
from user_management.verification.domain.factory import UserVerificationFactory
from user_management.verification.service_layer import exceptions as service_layer_exceptions
from user_management.verification.domain import exceptions as domain_layer_exceptions

class VerificationViewSet(ViewSet):

    @property
    def service(self) -> TokenService:
        return TokenService(
            repository=TokenRepository(),
            validator=TokenValidator(),
            factory=UserVerificationFactory()
        )

    @action(detail=False, methods=[HTTPMethod.POST])
    def resend_verification_email(self, request):
        try:
        
            self.service.resend_verification_email(
                email_or_username = request.data.get('email_or_username')
            )
            return Response(
                {'message': 'Verification email has been send. Please verify from email.'}, 
                status = status.HTTP_200_OK
            )
        
        except service_layer_exceptions.UnregisteredUser as e:
            return Response({'error': str(e)}, status = status.HTTP_404_NOT_FOUND)
        
        except (
            service_layer_exceptions.UserAlreadyVerified,
            service_layer_exceptions.TokenNotExpired,
            domain_layer_exceptions.InvalidToken
        ) as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=[HTTPMethod.PATCH])
    def verify(self, request):
        try:

            self.service.verify_token(
                token = request.data.get('token')
            )
            return Response(
                {'message': 'User has been verified. Please login with your email or username and password.'}, 
                status = status.HTTP_200_OK
            )
        
        except (
            service_layer_exceptions.TokenExpired, 
            service_layer_exceptions.UserAlreadyVerified
        ) as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)

        except service_layer_exceptions.TokenNotFound as e:
            return Response({'error': str(e)}, status = status.HTTP_404_NOT_FOUND)
