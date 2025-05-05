from rest_framework_simplejwt.views import TokenObtainPairView
from user_management.authentication.jwt.entrypoints.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):


    serializer_class = CustomTokenObtainPairSerializer
    
