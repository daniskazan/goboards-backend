from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from utils.generics.dto import Result


class MeetupUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session
