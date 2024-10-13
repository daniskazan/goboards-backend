from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import Response

from api.v1.oauth2.dependencies.oauth import (
    get_account_provider,
    get_jwt_service,
    get_oauth_service,
    get_redirect_link_provider,
)
from api.v1.oauth2.serializers.response.main import (
    AccessTokenData,
    AccessTokenVKResponse,
)
from core.auth.models import SessionORM
from core.oauth.models import SocialAccountORM
from core.oauth.services import (
    GenerateRefreshTokenInputData,
    JWTService,
    OAuthService,
)
from exceptions.app.auth import VKBadCodeException, VKBadRequestException
from oauth.providers.vk.account_provider import VKAccountProvider
from oauth.providers.vk.redirect_link_provider import VKRedirectLinkProvider
from utils.generics.dto import Result
from utils.generics.response import BadResponse, OkResponse


oauth2 = APIRouter(prefix="/oauth", tags=["Oauth"])


@oauth2.get(
    "/vk/callback",
)
async def callback(request: Request, code: str = Query()):
    return OkResponse.new(status_code=200, payload=code)


@oauth2.get("/vk/redirect-link", summary=" Перейти на страницу авторизации на стороне ВК")
async def get_vk_link(
    request: Request,
    provider: VKRedirectLinkProvider = Depends(get_redirect_link_provider),
):
    return OkResponse.new(status_code=status.HTTP_200_OK, payload=provider.redirect_link)


@oauth2.post(
    "/vk/login",
    summary="Авторизоваться через Вконтакте",
    name="auth:vk",
)
async def get_access_token(
    request: Request,
    response: Response,
    provider: VKAccountProvider = Depends(get_account_provider),
    oauth_service: OAuthService = Depends(get_oauth_service),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    vk_token: Result[AccessTokenVKResponse, None] | Result[None, VKBadCodeException] = await provider.get_access_token()
    match vk_token:
        case Result(None, VKBadCodeException() as err):
            return BadResponse.new(error=err.detail)

    profile: Result[dict, None] | Result[None, VKBadCodeException] = await provider.get_profile_info(vk_token)
    match profile:
        case Result(None, VKBadRequestException() as err):
            return BadResponse.new(error=err.detail)

    account: Result[SocialAccountORM, None] = await oauth_service.login(provider="vk", profile=profile)
    access_token: str = jwt_service.create_access_token(user=account.payload.user)
    session: SessionORM = await jwt_service.create_refresh_token(
        data=GenerateRefreshTokenInputData(
            user_id=account.payload.user_id,
            ip=request.client.host
        )
    )
    response.set_cookie(
        key="refreshToken",
        value=session.refresh_token,
        expires=session.expires_at.timestamp(),
        httponly=True,
    )
    return OkResponse.new(payload=AccessTokenData(access_token=access_token, refresh_token=session.refresh_token))
