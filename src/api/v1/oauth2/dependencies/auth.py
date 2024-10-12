import jwt

from fastapi import Depends
from fastapi.security import APIKeyHeader

from configs.server import ServerConfig
from core.oauth.services import UserAPIKeyCredentials
from exceptions.app.auth import AuthenticationRequiredHTTPException


api_key_header = APIKeyHeader(name="Authorization", description="Authorization token", auto_error=False)


async def get_user_or_401(
    api_token: str = Depends(api_key_header),
) -> UserAPIKeyCredentials:
    if not api_token:
        raise AuthenticationRequiredHTTPException
    try:
        payload = jwt.decode(api_token, ServerConfig.JWT_SECRET_KEY, algorithms=[ServerConfig.JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as exc:
        raise AuthenticationRequiredHTTPException from exc

    return UserAPIKeyCredentials(**payload)
