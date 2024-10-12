from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.games.models import GameORM
from core.games.repository.db.query_builders.get_games_list import (
    GetGameListQueryBuilder,
)
from exceptions.db.games import GameNotFoundException
from utils.generics.dto import Result


class GameReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_games_list(self, *, game_name: str | None, limit: int, offset: int) -> Result[list[GameORM], None]:
        q = GetGameListQueryBuilder.build(game_name=game_name, limit=limit, offset=offset)
        result = await self._session.execute(q)
        game_list = result.scalars().all()
        return Result.success(game_list)

    async def get_game_by_id(self, *, game_id: UUID) -> Result[GameORM, None] | Result[None, GameNotFoundException]:
        game: GameORM | None = await self._session.get(GameORM, game_id)
        if game:
            return Result.success(payload=game)
        return Result.failure(error=GameNotFoundException())
