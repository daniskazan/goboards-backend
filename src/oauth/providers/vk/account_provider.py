from typing import TypeAlias

import httpx
from api.v1.oauth2.serializers.response.main import AccessTokenVKResponse
from configs.oauth import oauth
from exceptions.app.auth import VKBadCodeException, VKBadRequestException
from oauth.providers.vk.access_token_provider import VKAccessTokenProvider
from utils.generics.dto import Result

USER_FIELDS = [
    "first_name",
    "last_name",
    "sex",
    "city",
    "country",
    "photo",
    "photo_medium",
    "photo_big",
    "photo_max_orig",
]

UserProfileInfo: TypeAlias = dict


class VKAccountProvider:
    VK_PROFILE_URL_FORMAT = "https://vk.com/id{vk_id}"
    PROFILE_URL = oauth.VK_PROFILE_URL
    VK_API_VERSION = oauth.VK_API_VERSION

    def __init__(self, *, access_token_provider: VKAccessTokenProvider) -> None:
        self._access_token_provider = access_token_provider

    async def get_access_token(self) -> Result[AccessTokenVKResponse, None] | Result[None, VKBadCodeException]:
        token = await self._access_token_provider.get_access_token()
        return token

    async def get_profile_info(self, result: Result[AccessTokenVKResponse, None]) -> Result[dict, None] | Result[None, VKBadCodeException]:
        async with httpx.AsyncClient() as c:
            response = await c.get(
                url=self.PROFILE_URL,
                params={
                    "access_token": result.payload.access_token,
                    "fields": ",".join(USER_FIELDS),
                    "v": self.VK_API_VERSION,
                },
            )
        if response.status_code:
            json: UserProfileInfo = response.json()["response"][0]
            profile_info: UserProfileInfo = self.update_profile_information(json, key="profile_url", value=self.VK_PROFILE_URL_FORMAT.format(vk_id=json["id"]))
            return Result.success(payload=profile_info)
        return Result.failure(error=VKBadRequestException())

    def update_profile_information(self, /, profile_info, *, key: str, value: str) -> UserProfileInfo:
        profile_info[key] = value
        return profile_info
