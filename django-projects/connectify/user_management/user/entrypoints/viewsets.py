from http import HTTPMethod

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from common.custom_pagination import CustomPagination
from events import message_bus
from user_management.user.service_layer.services import UserService
from user_management.user.service_layer.validator import UserValidator
from user_management.user.domain import exceptions as domain_exceptions
from user_management.user.service_layer import exceptions as services_exceptions
from user_management.common import exceptions as user_management_common_exceptions
from user_management.user.adapters.repository import UserRepository
from user_management.user.domain.factory import UserFactory

class UserViewSet(ViewSet):

    service_class = UserService
    paginator_class = CustomPagination
    permission_classes = [IsAuthenticated]

    @property
    def service(self) -> UserService:
        repository = UserRepository()
        validator = UserValidator(repository=repository)
        factory = UserFactory()

        return self.service_class(
            repository=repository, 
            validator=validator, 
            factory=factory, 
            message_bus=message_bus,
        )

    def list(self, request):
        user_filters = {
            'search_key': request.query_params.get('search_key'),
        }
        queryset = self.service.list_users(
            user_filters
        )
        paginator = self.paginator_class()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginator.get_paginated_response(data = paginated_queryset)


    def retrieve(self, request, pk):
        try:
            data = self.service.get_user(
                user_id=pk
            )
            return Response(
                data = data,
                status = status.HTTP_200_OK
            )
        except services_exceptions.UserNotFound as e:
            return Response(
                data = {'error': str(e)},
                status = status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=[HTTPMethod.POST], permission_classes=[AllowAny])
    def register(self, request):
        try:
            data = self.service.register_user(
                email=request.data.get("email"),
                password=request.data.get("password"),
                username=request.data.get("username"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
            )
            return Response(
                data = data,
                status = status.HTTP_201_CREATED
            )
        except (
            domain_exceptions.InvalidEmailLength, 
            user_management_common_exceptions.InvalidPasswordLength,
            domain_exceptions.InvalidUserFullNameLength,
            domain_exceptions.InvalidUserNameLength,
            services_exceptions.EmailAlreadyExists,
            services_exceptions.UserNameAlreadyExists
        ) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=[HTTPMethod.PATCH])
    def update_full_name(self, request, pk):
        try:
            data = self.service.update_full_name(
                user_id=pk,
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name")
            )
            return Response(
                data = data,
                status = status.HTTP_200_OK
            )
        except (domain_exceptions.InvalidUserFullNameLength) as e:
            return Response(
                data = {'error':str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
        except (services_exceptions.UserNotFound) as e:
            return Response(
                data = {'error': str(e)},
                status = status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk):
        try:
            self.service.delete_user(
                user_id=pk
            )
            return Response(
                data={'message': 'User Has Been Successfully Deleted.'},
                status = status.HTTP_200_OK
            )
        except (services_exceptions.UserNotFound) as e:
            return Response(
                data = {'error': str(e)},
                status = status.HTTP_404_NOT_FOUND
            )