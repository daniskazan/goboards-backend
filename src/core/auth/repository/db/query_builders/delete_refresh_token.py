import uuid

from typing import Self

from sqlalchemy.sql import Delete, delete

from core.auth.models import SessionORM


class DeleteRefreshSessionQueryBuilder:
    __result_query: Delete = ...

    @classmethod
    def __select_sessions(cls) -> type[Self]:
        cls.__result_query = delete(SessionORM)
        return cls

    @classmethod
    def __filter_by_value(cls, *, refresh_token: uuid.UUID) -> type[Self]:
        cls.__result_query = cls.__result_query.where(SessionORM.refresh_token == refresh_token)
        return cls

    @classmethod
    def __build(cls) -> Delete:
        return cls.__result_query

    @classmethod
    def build(cls, *, refresh_token: uuid.UUID) -> Delete:
        return cls.__select_sessions().__filter_by_value(refresh_token=refresh_token).__build()
