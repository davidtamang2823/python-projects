from rest_framework.routers import DefaultRouter

from chat.friend.entrypoints.viewsets import UserFriendViewSet

router = DefaultRouter()
router.register(r'friends', UserFriendViewSet, basename='user_friend')

urlpatterns = router.urls