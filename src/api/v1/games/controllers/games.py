from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from api.v1.games.dependencies.deps import (
    get_game_read_repo,
    get_game_service,
    has_permission_to_delete,
)
from api.v1.games.serializers.request.main import (
    CreateGameRequest,
    GetGameListRequest,
)
from api.v1.games.serializers.response.main import (
    CreateGameResponse,
    GetGameDetailResponse,
    GetGameListResponse,
)
from api.v1.oauth2.dependencies.auth import get_user_or_401
from core.games.services import GameService
from core.oauth.services import UserAPIKeyCredentials
from exceptions.db.games import GameNotFoundException
from utils.generics.dto import Result
from utils.generics.response import BadResponse, OkResponse


games = APIRouter(prefix="/games", tags=["Games"])


@games.get("/", summary="", name="game:list", response_model=OkResponse[GetGameListResponse])
async def get_games_list(
    request: Request,
    params: GetGameListRequest = Depends(),
    game_service: GameService = Depends(get_game_service),
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
):
    games_list = await game_service.get_games_list(params=params)
    return OkResponse.new(status_code=status.HTTP_200_OK, payload=GetGameListResponse.list_of_games(dto=games_list))


@games.get("/{game_id}", summary="", name="game:detail")
async def get_game_detail(
    request: Request, game_id: UUID, game_service: GameService = Depends(get_game_read_repo), user: UserAPIKeyCredentials = Depends(get_user_or_401)
):
    game = await game_service.get_game_by_id(game_id=game_id)
    match game:
        case Result(_, None):
            return OkResponse.new(payload=GetGameDetailResponse.get_detail_info(dto=game))
        case Result(None, GameNotFoundException() as error):
            return BadResponse.new(error=error.detail)


@games.delete("/", summary="", name="game:delete")
async def delete_game(
    request: Request,
    game_id: UUID,
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
    has_permission=Depends(has_permission_to_delete),
    game_service: GameService = Depends(get_game_service),
):
    await game_service.delete_game(game_id=game_id)
    return OkResponse.new(status_code=status.HTTP_204_NO_CONTENT, payload=None)


@games.post("/", summary="Create game", name="game:create")
async def create_game(
    request: Request,
    body: CreateGameRequest,
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
    game_service: GameService = Depends(get_game_service),
):
    result = await game_service.create_game(user_id=user.sub, game_name=body.name)
    return OkResponse.new(payload=CreateGameResponse.model_validate(result.payload))
