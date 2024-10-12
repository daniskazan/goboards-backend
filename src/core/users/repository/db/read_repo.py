import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from core.users.models import UserORM
from core.users.repository.db.query_builders.get_user_detail import (
    GetUserDetailQueryBuilder,
)
from exceptions.db.users import UserNotFoundException
from utils.generics.dto import Result


class UserReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_user_detail(self, *, user_id: uuid.UUID) -> Result[UserORM, None] | Result[None, UserNotFoundException]:
        q = GetUserDetailQueryBuilder.build(user_id=user_id)
        result = await self._session.execute(q)
        user: UserORM | None = result.scalar()
        if user:
            return Result.success(payload=user)
        return Result.failure(error=UserNotFoundException())
