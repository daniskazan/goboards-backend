import uuid

from configs.auth import auth
from core.auth.models import SessionORM
import datetime as dt
from sqlalchemy.ext.asyncio import AsyncSession
from utils.generics.dto import Result


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
            user_id=user_id, ip=ip,
            expires_at=dt.datetime.now() + dt.timedelta(seconds=auth.REFRESH_TOKEN_TTL)
        )
        self._session.add(session)
        await self._session.commit()
        return session

    async def delete_session(self, *, session: SessionORM) -> None:
        await self._session.delete(session)
        await self._session.commit()

