import jwt
from configs.server import server
from core.oauth.services import UserAPIKeyCredentials
from exceptions.app.auth import AuthenticationRequiredHTTPException
from fastapi import Depends
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization", description="Authorization token", auto_error=False)


async def get_user_or_401(
    api_token: str = Depends(api_key_header),
) -> UserAPIKeyCredentials:
    if not api_token:
        raise AuthenticationRequiredHTTPException
    try:
        payload = jwt.decode(api_token, server.JWT_SECRET_KEY, algorithms=[server.JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as exc:
        raise AuthenticationRequiredHTTPException from exc

    credentials = UserAPIKeyCredentials(**payload)
    return credentials
