import abc
import datetime as dt
import uuid
from dataclasses import dataclass
from typing import TypeAlias

import jwt

from configs.server import ServerConfig
from configs.auth import auth
from core.auth.models import SessionORM
from core.auth.repository.db.update_repo import SessionUpdateRepository
from core.oauth.exceptions import AccountNotFoundException
from core.oauth.models import SocialAccountORM
from core.oauth.repository.db.read_repo import SocialAccountReadRepository
from core.oauth.repository.db.update_repo import SocialAccountUpdateRepository
from core.users.models import UserORM
from core.users.repository.db.update_repo import UserUpdateRepository
from utils.generics.dto import Result
from utils.generics.response import PydanticBaseModel

UserProfileInfo: TypeAlias = dict
ProviderName: TypeAlias = str
SocialAccount: TypeAlias = Result[SocialAccountORM, None]
User: TypeAlias = Result[UserORM, None]


class UserAPIKeyCredentials(PydanticBaseModel):
    sub: uuid.UUID
    username: str
    exp: int


class GenerateRefreshTokenInputData(PydanticBaseModel):
    user_id: uuid.UUID
    ip: str


class JWTService(abc.ABC):
    @abc.abstractmethod
    def create_access_token(self, *, user: UserORM | UserAPIKeyCredentials) -> str: ...

    @abc.abstractmethod
    async def create_refresh_token(self, data: GenerateRefreshTokenInputData) -> SessionORM: ...


class JWTServiceImplementation(JWTService):
    def __init__(self, *, session_update_repo: SessionUpdateRepository):
        self._session_update_repo = session_update_repo

    def create_access_token(self, *, user: UserORM | UserAPIKeyCredentials) -> str:
        sub = user.sub if isinstance(user, UserAPIKeyCredentials) else user.id
        payload = UserAPIKeyCredentials(
            sub=sub,
            username=user.username,
            exp=int((dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(minutes=auth.ACCESS_TOKEN_TTL)).timestamp()),
        )
        return jwt.encode(
            payload=payload.model_dump(mode="json"),
            key=ServerConfig.JWT_SECRET_KEY,
            algorithm=ServerConfig.JWT_ALGORITHM
        )

    async def create_refresh_token(self, *, data: GenerateRefreshTokenInputData) -> SessionORM:
        res = await self._session_update_repo.create_session(user_id=data.user_id, ip=data.ip)
        return res


@dataclass(kw_only=True)
class OAuthService:
    read_repo: SocialAccountReadRepository
    update_repo: SocialAccountUpdateRepository
    user_update_repo: UserUpdateRepository

    async def _get_social_account(self, *, provider: str, user_id: int) -> Result[SocialAccountORM, None] | Result[None, AccountNotFoundException]:  # noqa
        account = await self.read_repo.get_social_account(provider_name=provider, user_id=user_id)
        return account

    async def _create_social_account(
        self,
        *,
        provider: ProviderName,
        user: Result[UserORM, None],
        extra_data: Result[dict, None],
    ) -> Result[SocialAccountORM, None]:
        account = await self.update_repo.create_social_account(provider=provider, user=user, extra_data=extra_data)
        return Result.success(payload=account)

    async def _perform_login(self, *, provider: ProviderName, profile: Result[dict, None]) -> Result[SocialAccountORM, None]:  # noqa
        social_account = await self._get_social_account(provider=provider, user_id=profile.payload.get("user_id"))
        if not social_account.payload:
            user = await self.user_update_repo.create_user_from_oauth_provider(profile_info=profile)
            social_account = await self._create_social_account(provider=provider, user=user, extra_data=profile)
        return social_account

    async def login(self, *, provider: ProviderName, profile: Result[dict, None]) -> Result[SocialAccountORM, None]:
        account = await self._perform_login(provider=provider, profile=profile)
        return account
