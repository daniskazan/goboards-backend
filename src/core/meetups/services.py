import uuid

from api.v1.meetups.serializers.request.main import GetMeetupListRequest
from core.meetups.models import MeetupORM
from exceptions.db.meetups import MeetupNotFoundException
from core.meetups.repository.db.read_repo import MeetupReadRepository
from utils.generics.dto import Result


class MeetupService:
    def __init__(self, *, meetup_read_repo: MeetupReadRepository):
        self.meetup_read_repo = meetup_read_repo

    async def get_meetup_list(self, *, params: GetMeetupListRequest) -> Result[list[MeetupORM], None]:
        return await self.meetup_read_repo.get_meetup_list(params=params)

    async def get_meetup_detail(self, *, meetup_id: uuid.UUID) -> Result[MeetupORM, None] | Result[None, MeetupNotFoundException]:
        return await self.meetup_read_repo.get_meetup_detail(meetup_id=meetup_id)
