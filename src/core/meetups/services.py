import uuid

from api.v1.meetups.serializers.request.main import (
    CreateMeetupRequest,
    GetMeetupListRequest,
)
from core.meetups.models import MeetupORM
from core.meetups.repository.db.read_repo import MeetupReadRepository
from core.meetups.repository.db.update_repo import MeetupUpdateRepository
from exceptions.db.meetups import MeetupNotFoundException
from utils.generics.dto import Result


class MeetupService:
    def __init__(self, *, meetup_read_repo: MeetupReadRepository, meetup_update_repo: MeetupUpdateRepository):
        self.meetup_read_repo = meetup_read_repo
        self.meetup_update_repo = meetup_update_repo

    async def get_meetup_list(self, *, params: GetMeetupListRequest) -> Result[list[MeetupORM], None]:
        return await self.meetup_read_repo.get_meetup_list(params=params)

    async def get_meetup_detail(self, *, meetup_id: uuid.UUID) -> Result[MeetupORM, None] | Result[None, MeetupNotFoundException]:
        return await self.meetup_read_repo.get_meetup_detail(meetup_id=meetup_id)

    async def create_meetup(self, *, params: CreateMeetupRequest):
        return await self.meetup_update_repo.create_meetup(params=params)
