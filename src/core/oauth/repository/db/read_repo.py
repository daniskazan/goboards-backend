from core.oauth.exceptions import AccountNotFoundException
from core.oauth.models import SocialAccountORM
from core.oauth.repository.db.query_builders.get_social_account import (
    GetSocialAccountQueryBuilder,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils.generics.dto import Result


class SocialAccountReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_social_account(self, provider_name: str, user_id: int) -> Result[SocialAccountORM, None] | Result[None, AccountNotFoundException]:
        q = GetSocialAccountQueryBuilder.build(provider=provider_name, user_id=user_id)
        result = await self._session.execute(q)
        account = result.scalar_one_or_none()
        if account:
            return Result.success(payload=account)
        return Result.failure(error=AccountNotFoundException)
