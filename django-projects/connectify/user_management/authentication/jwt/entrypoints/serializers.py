from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException
from django.contrib.auth import authenticate


class InvalidUserDetails(APIException):


    status_code = 401
    default_detail = "Invalid user details."
    default_code = "authentication_failed"


class UnverifiedUserAccount(APIException):


    status_code = 403
    default_detail = "Please verify your user account."
    default_code = "account_inactive"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):


    username_field='email_or_username'

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs[self.username_field],
            'password': attrs['password'],
        }
        
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        
        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise InvalidUserDetails
        
        if not self.user.is_active:
            raise UnverifiedUserAccount

        data = {}
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data