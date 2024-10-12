import datetime as dt
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from configs.auth import auth
from core.auth.models import SessionORM
from core.auth.repository.db.query_builders.delete_refresh_token import (
    DeleteRefreshSessionQueryBuilder,
)


class SessionUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_session(self, *, user_id: uuid.UUID, ip: str) -> SessionORM:
        session = SessionORM(
            id=uuid.uuid4(),
            user_id=user_id,
            ip=ip,
            expires_at=dt.datetime.now() + dt.timedelta(seconds=auth.REFRESH_TOKEN_TTL)  # noqa: DTZ005
        )
        self._session.add(session)
        await self._session.commit()
        return session

    async def delete_session(self, *, session: SessionORM) -> None:
        await self._session.delete(session)
        await self._session.commit()

    async def delete_session_by_value(self, *, refresh_token: uuid.UUID) -> None:
        q = DeleteRefreshSessionQueryBuilder.build(refresh_token=refresh_token)
        await self._session.execute(q)
        await self._session.commit()
