import datetime as dt
import uuid

from sqlalchemy import func, orm, types


class BaseORMModel(orm.DeclarativeBase):
    __abstract__ = True

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(types.UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=func.now())
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=func.now(), onupdate=func.now())
