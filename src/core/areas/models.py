from uuid import UUID

from sqlalchemy import ForeignKey, orm, UniqueConstraint
from utils.db.base import BaseORMModel


class AreaORM(BaseORMModel):
    __tablename__ = "areas"
    __table_args__ = (UniqueConstraint("name", "parent_id", name="name_parent_id_unique"),)

    name: orm.Mapped[str]
    parent_id: orm.Mapped[UUID] = orm.mapped_column(ForeignKey("areas.id"), nullable=True)

    areas: orm.Mapped[list["AreaORM"]] = orm.relationship("AreaORM")

    def __str__(self):
        return f"<{self.__class__.__name__}> {self.name}"
