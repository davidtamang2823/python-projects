from http import HTTPMethod
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from common.custom_pagination import CustomPagination
from chat.message.adapters.repository import PrivateMessageRepository
from chat.message.domain.factory import PrivateChatFactory
from chat.message.service_layer.services import PrivateChatService
from chat.friend.adapters.repository import UserFriendRepository
from chat.message.service_layer.validator import PrivateChatValidator


class PrivateChatViewSet(ViewSet):


    permission_classes = [IsAuthenticated]
    paginator_class = CustomPagination

    @property
    def service(self):
        return PrivateChatService(
            message_repository=PrivateMessageRepository(),
            chat_factory=PrivateChatFactory(),
            user_friend_repository=UserFriendRepository(),
            validator=PrivateChatValidator()
        )

    def get_paginated_response(self, queryset):
        paginator = self.paginator_class()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginator.get_paginated_response(data=paginated_queryset)

    @action(detail=False, methods=[HTTPMethod.GET])
    def get_private_messages(self, request):

        queryset = self.service.get_messages_between_users(
            request.user.id, 
            request.query_params.get('receiver_id')
        )
        return self.get_paginated_response(queryset)
    
    @action(detail=False, methods=[HTTPMethod.GET])
    def get_recent_messages(self, request):
        queryset = self.service.get_recent_messages(
            request.user.id
        )
        return self.get_paginated_response(queryset)