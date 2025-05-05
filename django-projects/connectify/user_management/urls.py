from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user_management.user.entrypoints.viewsets import UserViewSet
from user_management.verification.entrypoints.viewsets import VerificationViewSet, PasswordResetViewSet
from user_management.authentication.jwt.entrypoints.viewsets import CustomTokenObtainPairView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'verifications', VerificationViewSet, basename='verification')
router.register(r'passwordresets', PasswordResetViewSet, basename='password_reset')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/referesh/', TokenRefreshView.as_view(), name='token_refresh')
]