import datetime as dt
import uuid

from typing import Any, Self

from pydantic import Field, field_validator

from api.v1.games.serializers.response.main import NestedGameMeetupListResponse
from core.meetups.enums import MeetupStatus
from core.meetups.models import MeetupORM, MeetupUserORM
from utils.generics.dto import Result
from utils.generics.response import PydanticBaseModel


class GetMeetupListResponse(PydanticBaseModel):
    id: uuid.UUID = Field(alias="meetup_id")
    status: MeetupStatus = Field(alias="meetup_status")
    max_person_amount: int
    participant_count: int
    meetup_date: dt.date
    games: list[NestedGameMeetupListResponse]

    @classmethod
    def get_meetup_list(cls, /, result: Result[list[MeetupORM], None]) -> list[Self]:
        return [cls.model_validate(meet) for meet in result.payload]


class CreateMeetupResponse(PydanticBaseModel):
    id: uuid.UUID = Field(alias="meetup_id")
    area_id: uuid.UUID
    status: MeetupStatus = Field(alias="meetup_status")
    max_person_amount: int
    meetup_date: dt.date

    @classmethod
    def get_meetup(cls, /, result: Result[MeetupORM, None]) -> Self:
        return cls.model_validate(result.payload)


class MeetupParticipant(PydanticBaseModel):
    class MeetupUserStatus(PydanticBaseModel):
        user_status: str

    username: str = Field(...)
    meetup_associations: Any = Field(..., alias="user_status")
    id: uuid.UUID = Field(..., alias="user_id")

    @field_validator("meetup_associations")
    def display_user_meetup_status(cls, value: MeetupUserORM):  # noqa: N805
        return value.user_status.display()


class MeetupDetailResponse(GetMeetupListResponse):

    users: list[MeetupParticipant] = Field(alias="participants")

    @classmethod
    def from_orm(
        cls,
        meetup: MeetupORM,
    ):
        return cls.model_validate(meetup)
