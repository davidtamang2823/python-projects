from http import HTTPMethod

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorator import action
from rest_framework.response import Response

from common.paginator.paginator import PaginatorCommon
from events import message_bus
from user_management.user.service_layer.services import UserService
from user_management.user.service_layer.validator import UserValidator
from user_management.user.adapters.repository import UserRepository
from user_management.user.domain.factory import UserFactory

class UserViewSet(ViewSet):

    service_class = UserService

    def get_service(self) -> UserService:
        repository = UserRepository()
        validator = UserValidator(repository=repository)
        factory = UserFactory()
        paginator = PaginatorCommon()

        return self.service_class(
            repository=repository, 
            validator=validator, 
            factory=factory, 
            message_bus=message_bus,
            paginator=paginator
        )

    def list(self, request, *args, **kwargs):
        user_filters = {
            'page': request.query_params.get('page', 1),
            'page_size': request.query_params.get('page_size', 10),
            'search_key': request.query_params.get('search_key'),
        }
        paginated_details = self.get_service().list_users(
            user_filters
        )


    def retrive(self, request, *args, **kwargs):
        data = self.get_service().get_user(
            user_id=kwargs.get("pk")
        )
        return Response(
            data = data,
            status = status.HTTP_200_OK
        )

    @action(detail=False, methods=[HTTPMethod.POST])
    def register(self, request, *args, **kwargs):
        data = self.get_service().register_user(
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

    @action(detail=True, methods=[HTTPMethod.PATCH])
    def update_full_name(self, request, *args, **kwargs):
        data = self.get_service().update_full_name(
            user_id=kwargs.get("pk"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name")
        )
        return Response(
            data = data,
            status = status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        self.get_service().delete_user(
            user_id=kwargs.get("pk")
        )
        return Response(
            data={'message': 'User Has Been Successfully Deleted.'},
            status = status.HTTP_200_OK
        )