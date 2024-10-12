from fastapi import Body, Depends

from api.v1.oauth2.serializers.request.main import UserLoginVKRequest
from core.auth.repository.db.read_repo import SessionReadRepository
from core.auth.repository.db.update_repo import SessionUpdateRepository
from core.oauth.repository.db.read_repo import SocialAccountReadRepository
from core.oauth.repository.db.update_repo import SocialAccountUpdateRepository
from core.oauth.services import (
    JWTService,
    JWTServiceImplementation,
    OAuthService,
)
from core.users.repository.db.update_repo import UserUpdateRepository
from oauth.providers.vk.access_token_provider import VKAccessTokenProvider
from oauth.providers.vk.account_provider import VKAccountProvider
from oauth.providers.vk.redirect_link_provider import VKRedirectLinkProvider
from utils.db.session import get_db


def get_redirect_link_provider() -> VKRedirectLinkProvider:
    return VKRedirectLinkProvider()


def get_access_token_provider(
    params: UserLoginVKRequest = Body(...),
) -> VKAccessTokenProvider:
    return VKAccessTokenProvider(code=params.code)


def get_account_provider(
    token_provider: VKAccessTokenProvider = Depends(get_access_token_provider),
) -> VKAccountProvider:
    return VKAccountProvider(access_token_provider=token_provider)


def get_social_account_read_repo(session=Depends(get_db)):
    return SocialAccountReadRepository(session=session)


def get_social_account_update_repo(session=Depends(get_db)):
    return SocialAccountUpdateRepository(session=session)


def get_user_update_repo(session=Depends(get_db)):
    return UserUpdateRepository(session=session)


def get_oauth_service(
    read_repo=Depends(get_social_account_read_repo),
    update_repo=Depends(get_social_account_update_repo),
    user_update_repo=Depends(get_user_update_repo),
) -> OAuthService:
    return OAuthService(read_repo=read_repo, update_repo=update_repo, user_update_repo=user_update_repo)


def get_session_update_repo(session=Depends(get_db)) -> SessionUpdateRepository:
    return SessionUpdateRepository(session=session)


def get_session_read_repo(session=Depends(get_db)) -> SessionReadRepository:
    return SessionReadRepository(session=session)


def get_jwt_service(session_update_repo: SessionUpdateRepository = Depends(get_session_update_repo)) -> JWTService:
    return JWTServiceImplementation(session_update_repo=session_update_repo)
