from rest_framework.routers import DefaultRouter

from user_management.user.entrypoints.viewsets import UserViewSet
from user_management.verification.entrypoints.viewsets import VerificationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='apiuser')
router.register(r'verifications', VerificationViewSet, basename='apiuserverification')
urlpatterns = router.urls