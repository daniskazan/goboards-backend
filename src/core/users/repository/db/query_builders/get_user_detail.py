import uuid

from typing import Self

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select

from core.users.models import UserORM


class GetUserDetailQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_users(cls) -> type[Self]:
        cls.__result_query = select(UserORM)
        return cls

    @classmethod
    def __filter_by_user_id(cls, *, user_id: int) -> type[Self]:
        cls.__result_query = cls.__result_query.where(UserORM.id == user_id)
        return cls

    @classmethod
    def __join_social_links(cls) -> type[Self]:
        cls.__result_query = cls.__result_query.options(selectinload(UserORM.social_accounts))
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, user_id: uuid.UUID) -> Select:
        return cls.__select_users().__filter_by_user_id(user_id=user_id).__join_social_links().__build()
