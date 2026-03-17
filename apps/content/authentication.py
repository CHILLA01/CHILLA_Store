import jwt
from datetime import datetime, timedelta, timezone

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            return (user, token)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid or expired token")


class SuperUserAuth(BaseAuthentication):
    def authenticate(self, request):
        result = TokenAuth().authenticate(request)
        if result is None:
            return None
        user, token = result
        if not user.is_superuser:
            raise AuthenticationFailed("Superuser access required")
        return (user, token)