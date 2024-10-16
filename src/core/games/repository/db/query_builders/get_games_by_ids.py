from typing import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from core.games.models import GameORM


class GetGamesByIdsQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_games(cls) -> type[Self]:
        cls.__result_query = select(GameORM)
        return cls

    @classmethod
    def __filter_by_ids(cls, game_ids: list[UUID]) -> type[Self]:
        cls.__result_query = cls.__result_query.where(GameORM.id.in_(game_ids))
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, game_ids: list[UUID]) -> Select:
        return cls.__select_games().__filter_by_ids(game_ids=game_ids).__build()
