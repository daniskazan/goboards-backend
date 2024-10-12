from uuid import UUID

from fastapi import Depends

from api.v1.oauth2.dependencies.auth import get_user_or_401
from core.games.repository.db.read_repo import GameReadRepository
from core.games.repository.db.update_repo import GameUpdateRepository
from core.games.services import GameService
from core.oauth.services import UserAPIKeyCredentials
from exceptions.app.auth import ForbiddenHTTPException
from utils.db.session import get_db
from utils.generics.dto import Result


def get_game_read_repo(session=Depends(get_db)):
    return GameReadRepository(session=session)


def get_game_update_repo(session=Depends(get_db)):
    return GameUpdateRepository(session=session)


def get_game_service(game_read_repo=Depends(get_game_read_repo), game_update_repo=Depends(get_game_update_repo)):
    return GameService(game_read_repo=game_read_repo, game_update_repo=game_update_repo)


async def has_permission_to_delete(
    game_id: UUID, game_read_repo: GameReadRepository = Depends(get_game_read_repo), user: UserAPIKeyCredentials = Depends(get_user_or_401)
) -> bool:
    game = await game_read_repo.get_game_by_id(game_id=game_id)
    match game:
        case Result(_, None):
            if not game.payload.user_id:
                raise ForbiddenHTTPException
            game_owner: bool = str(game.payload.user_id) == user.sub
            if not game_owner:
                raise ForbiddenHTTPException
    return True
