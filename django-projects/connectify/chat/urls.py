from rest_framework.routers import DefaultRouter

from chat.friend.entrypoints.viewsets import UserFriendViewSet
from chat.message.entrypoints.viewsets import PrivateChatViewSet

router = DefaultRouter()
router.register(r'friends', UserFriendViewSet, basename='user_friend')
router.register(r'private_chats', PrivateChatViewSet, basename='private_chat')

urlpatterns = router.urls