import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.meetups.serializers.request.main import GetMeetupListRequest
from core.meetups.models import MeetupORM
from exceptions.db.meetups import MeetupNotFoundException
from core.meetups.repository.db.query_builders.get_meetups_list import GetMeetupListQueryBuilder
from core.meetups.repository.db.query_builders.get_meetup_detail import GetMeetupDetailQueryBuilder
from utils.generics.dto import Result


class MeetupReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_meetup_list(self, *, params: GetMeetupListRequest) -> Result[list[MeetupORM], None]:
        q = GetMeetupListQueryBuilder.build(meetup_date=params.date, limit=params.limit, offset=params.offset)
        res = await self._session.execute(q)
        meetup_list = res.scalars().all()
        return Result.success(payload=meetup_list)

    async def get_meetup_detail(self, *, meetup_id: uuid.UUID) -> Result[MeetupORM, None] | Result[None, MeetupNotFoundException]:
        q = GetMeetupDetailQueryBuilder.build(meetup_id=meetup_id)
        result = await self._session.execute(q)
        meetup = result.scalar_one_or_none()
        if not meetup:
            return Result.failure(error=MeetupNotFoundException)
        return Result.success(payload=meetup)
