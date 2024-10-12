from uuid import UUID

from sqlalchemy import ForeignKey, orm

from core.games.enums import GameType
from core.users.models import UserORM
from utils.db.base import BaseORMModel


class GameORM(BaseORMModel):
    __tablename__ = "games"
    name: orm.Mapped[str] = orm.mapped_column(nullable=False, unique=True)
    game_type: orm.Mapped[GameType] = orm.mapped_column(default=GameType.USER, nullable=False)
    user_id: orm.Mapped[UUID] = orm.mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    user: orm.Mapped["UserORM"] = orm.relationship(
        back_populates="games", lazy="joined"
    )
