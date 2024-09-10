import uuid

from sqlalchemy import orm
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

import datetime as dt

from core.areas.models import AreaORM
from core.games.models import GameORM
from core.meetups.enums import MeetupStatus, UserMeetupStatus
from core.users.models import UserORM
from utils.db.base import BaseORMModel


class MeetupUserORM(BaseORMModel):
    __tablename__ = "meetups_users"
    __table_args__ = (UniqueConstraint("meetup_id", "user_id", name="meetup_user_unique"),)
    meetup_id: orm.Mapped[uuid.UUID] = orm.mapped_column(ForeignKey("meetups.id"))
    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(ForeignKey("users.id"))
    user_status: orm.Mapped[UserMeetupStatus]


class MeetupGameORM(BaseORMModel):
    __tablename__ = "meetups_games"
    __table_args__ = (UniqueConstraint("meetup_id", "game_id", name="meetup_game_unique"),)
    meetup_id: orm.Mapped[uuid.UUID] = orm.mapped_column(ForeignKey("meetups.id"))
    game_id: orm.Mapped[uuid.UUID] = orm.mapped_column(ForeignKey("games.id"))


class MeetupORM(BaseORMModel):
    __tablename__ = "meetups"

    meetup_status: orm.Mapped[MeetupStatus] = orm.mapped_column(default=MeetupStatus.NEW)
    area_id: orm.Mapped[uuid.UUID] = orm.mapped_column(ForeignKey("areas.id"), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(default=None, nullable=True)
    max_person_amount: orm.Mapped[int] = orm.mapped_column(nullable=False)
    meetup_date: orm.Mapped[dt.date] = orm.mapped_column(nullable=False)
    preferred_start_time: orm.Mapped[dt.time] = orm.mapped_column(nullable=False)
    preferred_end_time: orm.Mapped[dt.time] = orm.mapped_column(nullable=False)

    area: orm.Mapped[AreaORM] = orm.relationship(lazy="joined")
    games: orm.Mapped[list[GameORM]] = orm.relationship(secondary="meetups_games")
    users: orm.Mapped[list[UserORM]] = orm.relationship(secondary="meetups_users")

    @property
    def participant_count(self) -> int:
        return len(self.users)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> #{self.id}"
