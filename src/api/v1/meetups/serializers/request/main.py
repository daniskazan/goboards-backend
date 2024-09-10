import datetime as dt
import uuid

from fastapi import Query
from pydantic import Field, PositiveInt, StrictInt

from core.meetups.enums import MeetupStatus
from utils.generics.response import PydanticBaseModel


class GetMeetupListRequest(PydanticBaseModel):
    date: dt.date = Field(default=dt.date.today(), description="Date of meetup(default is today)")
    limit: PositiveInt = Field(default=Query(default=100))
    offset: StrictInt = Field(default=Query(default=0))


class CreateMeetupRequest(PydanticBaseModel):
    meetup_date: dt.date = Field(default=dt.date.today(), description="Date of meetup(default is today)")
    max_person_amount: PositiveInt = Field(default=2, ge=2)
    preferred_start_time: dt.time = Field(..., description="Желаемое время начала встречи")
    preferred_end_time: dt.time = Field(..., description="Желаемое время окончания встречи")
    description: str | None = Field(default=None, description="Доп. информация по встрече")
    area_id: uuid.UUID = Field(..., description="Идентификатор города")
