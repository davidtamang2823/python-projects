from http import HTTPMethod

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.friend.service_layer import exceptions as service_layer_exceptions
from chat.friend.domain import exceptions as domain_layer_exceptions
from chat.friend.domain.factory import UserFriendFactory
from chat.friend.adapters.repository import UserFriendRepository
from chat.friend.service_layer.services import UserFriendService
from chat.friend.service_layer.validator import UserFriendValidator
from common.custom_pagination import CustomPagination


class UserFriendViewSet(ViewSet):


    service_class = UserFriendService
    permission_classes = [IsAuthenticated]
    paginator_class = CustomPagination

    @property
    def service(self) -> UserFriendService:
        repository = UserFriendRepository()
        validator = UserFriendValidator()
        factory = UserFriendFactory()

        return self.service_class(
            repository=repository, 
            validator=validator, 
            factory=factory, 
        )

    def list(self, request):
        list_filter = {
            'search_key': request.query_params.get('search_key')
        }
        queryset = self.service.get_friends_list(
            user_id=request.user.id,
            list_filter=list_filter
        )
        paginator = self.paginator_class()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginator.get_paginated_response(data = paginated_queryset)
    
    @action(detail=False, methods=[HTTPMethod.GET])
    def get_friend_requests(self, request):
        list_filter = {
            'search_key': request.query_params.get('search_key')
        }
        queryset = self.service.get_friend_requests(
            user_id=request.user.id,
            list_filter=list_filter
        )
        paginator = self.paginator_class()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginator.get_paginated_response(data = paginated_queryset)

    @action(detail=False, methods=[HTTPMethod.POST])
    def send_friend_request(self, request):
        try:
            self.service.send_friend_request(
                user_id=request.user.id,
                friend_id=request.data.get('friend_id')
            )
            return Response(
                data = {
                    'message': 'Friend request has been sent successfully.'
                },
                status = status.HTTP_201_CREATED
            )
        except (
            service_layer_exceptions.FriendRequestAccepted, 
            service_layer_exceptions.FriendRequestPending,
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=[HTTPMethod.PATCH])
    def accept_friend_request(self, request):
        try:
            self.service.accept_friend_request(
                user_id=request.user.id,
                friend_id=request.data.get('friend_id'),
                status='accepted'
            )
            return Response(
                data = {
                    'message': 'Friend request has been accepted.'
                },
                status = status.HTTP_201_CREATED
            )
        except(
            service_layer_exceptions.FriendDoesNotExists,
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=[HTTPMethod.PATCH])
    def reject_friend_request(self, request):
        try:
            self.service.reject_friend_request(
                user_id=request.user.id,
                friend_id=request.data.get('friend_id'),
                status='rejected'
            )
            return Response(
                data = {
                    'message': 'Friend request has been rejected.'
                },
                status = status.HTTP_201_CREATED
            )
        except(
            service_layer_exceptions.FriendDoesNotExists,
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
        

    @action(detail=False, methods=[HTTPMethod.PATCH])
    def block_friend(self, request):
        try:
            self.service.block_friend(
                user_id=request.user.id,
                friend_id=request.data.get('friend_id'),
                status='blocked'
            )
            return Response(
                data = {
                    'message': 'Friend request has been rejected.'
                },
                status = status.HTTP_201_CREATED
            )
        except(
            service_layer_exceptions.FriendDoesNotExists,
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=[HTTPMethod.PATCH])
    def unblock_friend(self, request):
        try:
            self.service.unblock_friend(
                user_id=request.user.id,
                friend_id=request.data.get('friend_id'),
                status='accepted'
            )
            return Response(
                data = {
                    'message': 'User has been unblocked.'
                },
                status = status.HTTP_201_CREATED
            )
        except(
            service_layer_exceptions.FriendDoesNotExists,
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=[HTTPMethod.DELETE])
    def remove_friendship(self, request, *args, **kwargs):
        try:
            self.service.remove_friend(
                user_id=request.user.id,
                friend_id=kwargs.get('pk')
            )
            return Response(
                data = {
                    'message': 'User has been removed from your friends list.'
                },
                status = status.HTTP_201_CREATED
            )
        except(
            domain_layer_exceptions.SameUserFriendId
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
