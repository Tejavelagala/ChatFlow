"""
Custom JWT Authentication Middleware for Django Channels WebSocket
"""
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token_string):
    """
    Validate JWT token and return user
    """
    try:
        logger.debug("WSJWT validating token length=%d prefix=%s", len(token_string), token_string[:20])
        access_token = AccessToken(token_string)
        user_id = access_token['user_id']

        user = User.objects.get(id=user_id, is_active=True)
        logger.debug("WSJWT authenticated user_id=%s username=%s", user.id, user.username)
        return user
    except (InvalidToken, TokenError) as e:
        logger.warning("WSJWT authentication failed token_error=%s token_length=%d", str(e), len(token_string))
        return AnonymousUser()
    except User.DoesNotExist as e:
        logger.warning("WSJWT authentication failed reason=user_not_found user_id=%s", user_id)
        return AnonymousUser()
    except Exception as e:
        logger.error("WSJWT authentication failed unexpected_error=%s", str(e))
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate WebSocket connections using JWT
    """
    
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)

        token = query_params.get('token', [None])[0]
        token_source = 'query' if token else None

        if not token:
            headers = dict(scope.get('headers') or [])
            authorization = headers.get(b'authorization', b'').decode()
            if authorization.lower().startswith('bearer '):
                token = authorization.split(' ', 1)[1].strip()
                token_source = 'authorization_header'

        logger.debug(
            "WSJWT path=%s token_present=%s token_source=%s",
            scope.get('path'),
            bool(token),
            token_source,
        )

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            logger.warning("WSJWT missing token path=%s", scope.get('path'))
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    """
    Convenience function to wrap URLRouter with JWT authentication
    """
    return JWTAuthMiddleware(inner)
