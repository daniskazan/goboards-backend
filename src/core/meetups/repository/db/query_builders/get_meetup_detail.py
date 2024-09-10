import uuid
from typing import Self
import datetime as dt
from core.meetups.models import MeetupORM, MeetupGameORM
from core.meetups.enums import MeetupStatus
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select


class GetMeetupDetailQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_meetups(cls) -> type[Self]:
        cls.__result_query = select(MeetupORM)
        return cls

    @classmethod
    def __filter_by_id(cls, *, meetup_id: uuid.UUID) -> type[Self]:
        cls.__result_query = cls.__result_query.where(MeetupORM.id == meetup_id)
        return cls

    @classmethod
    def __join_games(cls):
        cls.__result_query = cls.__result_query.join(MeetupORM.games)
        return cls

    @classmethod
    def __join_users(cls):
        cls.__result_query = cls.__result_query.join(MeetupORM.users)
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, meetup_id: uuid.UUID) -> Select:
        q = (
            cls.__select_meetups()
            .__filter_by_id(meetup_id=meetup_id)
            .__join_games()
            .__join_users()
            .__build()
        )
        return q
