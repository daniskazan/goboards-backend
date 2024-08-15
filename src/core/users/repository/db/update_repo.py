from core.users.models import UserORM
from sqlalchemy.ext.asyncio import AsyncSession
from utils.generics.dto import Result


class UserUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_user_from_oauth_provider(self, *, profile_info: Result[dict, None]) -> Result[UserORM, None]:
        user = UserORM(
            first_name=profile_info.payload.get("first_name"),
            last_name=profile_info.payload.get("last_name"),
        )
        self._session.add(user)
        await self._session.commit()
        return Result.success(payload=user)
