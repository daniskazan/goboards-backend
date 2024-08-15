from core.users.models import UserORM
from sqlalchemy import ForeignKey, UniqueConstraint, orm, types
from utils.db.base import BaseORMModel


class SocialAccountORM(BaseORMModel):
    __tablename__ = "social_accounts"
    __table_args__ = (UniqueConstraint("provider", "user_id", name="provider_user_id_unique"),)
    provider: orm.Mapped[str]
    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    extra_data: orm.Mapped[dict] = orm.mapped_column(types.JSON)

    user: orm.Mapped["UserORM"] = orm.relationship(back_populates="social_accounts", lazy="joined")

    @property
    def profile_url(self):
        return self.extra_data.get("profile_url", None)
