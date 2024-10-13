from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.meetups.serializers.request.main import CreateMeetupRequest
from core.games.repository.db.query_builders.get_games_by_ids import (
    GetGamesByIdsQueryBuilder,
)
from core.meetups.models import MeetupORM
from core.users.models import UserORM
from utils.generics.dto import Result


class MeetupUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_meetup(self, *, user_id: UUID, params: CreateMeetupRequest) -> Result[MeetupORM, None]:
        user = await self._session.get(UserORM, user_id)
        games = (await self._session.execute(
            GetGamesByIdsQueryBuilder.build(game_ids=params.game_ids)
        )).scalars().all()
        if not games:
            raise IntegrityError("Games not found")

        meetup = MeetupORM(
            area_id=params.area_id,
            description=params.description,
            max_person_amount=params.max_person_amount,
            meetup_date=params.meetup_date,
            preferred_start_time=params.preferred_start_time,
            preferred_end_time=params.preferred_end_time,
        )
        meetup.users.append(user)
        meetup.games.append(*games)
        self._session.add(meetup)
        await self._session.commit()
        return Result.success(payload=meetup)
