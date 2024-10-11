from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.meetups.serializers.request.main import CreateMeetupRequest
from core.meetups.models import MeetupORM
from utils.generics.dto import Result


class MeetupUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_meetup(self, *, params: CreateMeetupRequest) -> Result[MeetupORM, None]:
        meetup = MeetupORM(
            area_id=params.area_id,
            description=params.description,
            max_person_amount=params.max_person_amount,
            meetup_date=params.meetup_date,
            preferred_start_time=params.preferred_start_time,
            preferred_end_time=params.preferred_end_time,
        )
        self._session.add(meetup)
        await self._session.commit()
        return Result.success(payload=meetup)
