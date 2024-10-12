from sqlalchemy.ext.asyncio import AsyncSession

from core.oauth.models import SocialAccountORM
from core.users.models import UserORM
from utils.generics.dto import Result


type UserProfileInfo = Result[dict, None]


class SocialAccountUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_social_account(
        self,
        *,
        provider: str,
        user: Result[UserORM, None],
        extra_data: Result[UserProfileInfo, None],
    ) -> SocialAccountORM:
        account = SocialAccountORM(
            provider=provider,
            extra_data=extra_data.payload,
            user_id=user.payload.id,
        )
        self._session.add(account)
        await self._session.commit()
        return account
