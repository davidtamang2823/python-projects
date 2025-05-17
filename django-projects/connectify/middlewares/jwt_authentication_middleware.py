import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from user_management.user.adapters.repository import UserRepository


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.user_repository = UserRepository()

    async def __call__(self, scope, receive, send):
        try:
            headers = dict(scope.get("headers", []))
            auth_header = headers.get(b'authorization', b'').decode()
            
            if not auth_header.startswith('Bearer '):
                raise ValueError("Missing Bearer token")
            
            token = auth_header[7:]
            user = await self.get_user_from_token(token)
            
            if not user or not user.is_authenticated:
                raise ValueError("Invalid user")
            
            scope['user'] = user
            return await super().__call__(scope, receive, send)

        except Exception:
            await self._reject_connection(send)
            return

    async def _reject_connection(self, send):
        await send({
            'type': 'websocket.close',
            'code': 4001  # Unauthorized
        })

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            if user_id:
                user = self.user_repository.get_by_id_object(user_id)
                if user and user.is_active:
                    return user
        except (
            jwt.ExpiredSignatureError, 
            jwt.InvalidTokenError,
            Exception
        ):
            pass
        return AnonymousUser()