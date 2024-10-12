import datetime as dt

from typing import Self

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select

from core.meetups.enums import MeetupStatus
from core.meetups.models import MeetupORM


class GetMeetupListQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_meetups(cls) -> type[Self]:
        cls.__result_query = select(
            MeetupORM,
        )
        return cls

    @classmethod
    def __join_games(cls):
        cls.__result_query = cls.__result_query.options(selectinload(MeetupORM.games))
        return cls

    @classmethod
    def __join_users(cls):
        cls.__result_query = cls.__result_query.options(selectinload(MeetupORM.users))
        return cls

    @classmethod
    def __filter_by_status(cls):
        cls.__result_query = cls.__result_query.where(MeetupORM.meetup_status.in_((MeetupStatus.NEW, MeetupStatus.DISCUSSION)))
        return cls

    @classmethod
    def __filter_by_date(cls, *, meetup_date: dt.date):
        cls.__result_query = cls.__result_query.where(MeetupORM.meetup_date == meetup_date)
        return cls

    @classmethod
    def __order_by_status(cls):
        cls.__result_query = cls.__result_query.order_by(MeetupORM.meetup_status)

    @classmethod
    def __apply_limit_offset(cls, *, limit: int, offset: int) -> type[Self]:
        cls.__result_query = cls.__result_query.limit(limit=limit).offset(offset=offset)
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(
        cls,
        *,
        meetup_date: dt.date,
        limit: int,
        offset: int,
    ) -> Select:
        return (
            cls.__select_meetups()
            .__join_games()
            .__join_users()
            .__filter_by_status()
            .__filter_by_date(meetup_date=meetup_date)
            .__apply_limit_offset(limit=limit, offset=offset)
            .__build()
        )
