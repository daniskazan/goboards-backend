import enum
import urllib.parse

import httpx

from api.v1.oauth2.serializers.response.main import AccessTokenVKResponse
from configs.oauth.vk import VKOauthConfig
from exceptions.app.auth import VKBadCodeException
from utils.generics.dto import Result


class RequestStatus(int, enum.Enum):
    SUCCESS = 200


class VKAccessTokenProvider:
    def __init__(
        self,
        *,
        code: str,
    ) -> None:
        self._code = code
        self._access_token_base_url = VKOauthConfig.VK_ACCESS_TOKEN_URL
        self._client_id = VKOauthConfig.VK_CLIENT_ID
        self._client_secret = VKOauthConfig.VK_SECRET_KEY
        self._redirect_uri = VKOauthConfig.VK_REDIRECT_URI

    @property
    def access_token_url(self) -> str:
        params = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "code": self._code,
        }
        return self._access_token_base_url + urllib.parse.urlencode(params)

    async def get_access_token(
        self,
    ) -> Result[AccessTokenVKResponse, None] | Result[None, VKBadCodeException]:
        async with httpx.AsyncClient() as c:
            response = await c.get(
                self._access_token_base_url,
                params={
                    "code": self._code,
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "redirect_uri": self._redirect_uri,
                },
            )
            match response.status_code:
                case RequestStatus.SUCCESS:
                    return Result.success(payload=AccessTokenVKResponse(**response.json()))
                case _:
                    return Result.failure(error=VKBadCodeException())
