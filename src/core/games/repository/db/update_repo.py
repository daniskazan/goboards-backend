from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.games.models import GameORM
from utils.generics.dto import Result


class GameUpdateRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def delete_game(self, *, result: Result[GameORM, None]) -> Result[bool, None]:
        await self._session.delete(result.payload)
        await self._session.commit()
        return Result.success(True)

    async def create_game(self, *, user_id: UUID, game_name: str) -> Result[GameORM, None]:
        game = GameORM(name=game_name, user_id=user_id)
        self._session.add(game)
        await self._session.commit()
        return Result.success(payload=game)
