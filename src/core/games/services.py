from uuid import UUID

from api.v1.games.serializers.request.main import GetGameListRequest
from core.games.models import GameORM
from core.games.repository.db.read_repo import GameReadRepository
from core.games.repository.db.update_repo import GameUpdateRepository
from exceptions.db.games import GameNotFoundException
from utils.generics.dto import Result


class GameService:
    def __init__(self, *, game_read_repo: GameReadRepository, game_update_repo: GameUpdateRepository) -> None:
        self.game_read_repo = game_read_repo
        self.game_update_repo = game_update_repo

    async def get_game_by_id(self, *, game_id: UUID) -> Result[GameORM, None] | Result[None, GameNotFoundException]:
        game = await self.game_read_repo.get_game_by_id(game_id=game_id)
        return game

    async def get_games_list(self, *, params: GetGameListRequest) -> Result[list[GameORM], None]:
        return await self.game_read_repo.get_games_list(game_name=params.name, limit=params.limit, offset=params.offset)

    async def delete_game(self, *, game_id: UUID) -> Result[bool, None] | Result[None, GameNotFoundException]:
        result = await self.game_read_repo.get_game_by_id(game_id=game_id)
        if not result.payload:
            return result

        return await self.game_update_repo.delete_game(result=result)

    async def create_game(self, *, user_id: UUID, game_name: str) -> Result[GameORM, None]:
        game = await self.game_update_repo.create_game(user_id=user_id, game_name=game_name)
        return game
