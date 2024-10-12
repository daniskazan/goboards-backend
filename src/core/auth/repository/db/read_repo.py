import datetime
import datetime as dt
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth.models import SessionORM
from exceptions.db.auth import SessionNotFoundException
from utils.generics.dto import Result


class SessionReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_session_by_id(self, *, user_id: uuid.UUID, refresh_token: uuid.UUID) -> Result[SessionORM, None] | Result[None, SessionNotFoundException]:
        q = (
            select(SessionORM)
            .where(SessionORM.expires_at > dt.datetime.now(tz=datetime.UTC))
            .where(SessionORM.refresh_token == refresh_token)
            .where(SessionORM.user_id == user_id)
        )
        session = await self._session.execute(q)
        if session_scalar := session.scalar_one_or_none():
            return Result.success(payload=session_scalar)
        return Result.failure(error=SessionNotFoundException())
