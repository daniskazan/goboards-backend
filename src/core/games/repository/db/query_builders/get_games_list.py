from typing import Self

from core.games.models import GameORM
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select


class GetGameListQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_banners(cls) -> type[Self]:
        cls.__result_query = select(GameORM)
        return cls

    @classmethod
    def __filter_by_name(cls, *, game_name: str | None) -> type[Self]:
        if game_name:
            cls.__result_query = cls.__result_query.where(GameORM.name.like(game_name))
        return cls

    @classmethod
    def __apply_limit_offset(cls, *, limit: int, offset: int) -> type[Self]:
        cls.__result_query = cls.__result_query.limit(limit=limit).offset(offset=offset)
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, game_name: str | None, limit: int, offset: int) -> Select:
        q = cls.__select_banners().__filter_by_name(game_name=game_name).__apply_limit_offset(limit=limit, offset=offset).__build()
        return q
