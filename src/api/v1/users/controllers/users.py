import uuid

from fastapi import APIRouter, Depends, Request, status

from api.v1.oauth2.dependencies.auth import get_user_or_401
from api.v1.users.dependencies.deps import get_user_service
from api.v1.users.serializers.response.main import GetUserDetailResponse
from core.oauth.services import UserAPIKeyCredentials
from core.users.services import UserService
from exceptions.db.users import UserNotFoundException
from utils.generics.dto import Result
from utils.generics.response import BadResponse, OkResponse


users = APIRouter(prefix="/users", tags=["Users"])


@users.get(
    "/me",
    summary="",
)
async def get_current_user_info(
    request: Request,
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
):
    return OkResponse.new(payload=user)


@users.get("/{user_id}", summary="Информация по юзеру")
async def get_user_detail(request: Request, user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)):
    result = await user_service.get_user_detail(user_id=user_id)
    match result:
        case Result(None, UserNotFoundException() as err):
            return BadResponse.new(status_code=status.HTTP_404_NOT_FOUND, error=err.detail)
        case Result(_, None):
            return OkResponse.new(payload=GetUserDetailResponse.get_user_detail_info(result))
