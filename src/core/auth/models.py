from utils.db.base import BaseORMModel
from core.users.models import UserORM
import datetime as dt
import uuid
from sqlalchemy import ForeignKey, UniqueConstraint, orm, types


class SessionORM(BaseORMModel):
    __tablename__ = "sessions"
    updated_at = None

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ip: orm.Mapped[str] = orm.mapped_column(nullable=False)
    refresh_token: orm.Mapped[uuid.UUID] = orm.mapped_column(default=uuid.uuid4(), nullable=False)
    user: orm.Mapped["UserORM"] = orm.relationship(back_populates="sessions", lazy="joined")
    expires_at: orm.Mapped[dt.datetime] = orm.mapped_column(nullable=False)
