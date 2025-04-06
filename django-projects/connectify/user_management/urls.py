from rest_framework.routers import DefaultRouter

from user_management.user.entrypoints.viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='apiuser')

urlpatterns = router.urls