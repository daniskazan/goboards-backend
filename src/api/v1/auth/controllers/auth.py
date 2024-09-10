import uuid
from fastapi import APIRouter, Depends, Request, status, Cookie
from fastapi.responses import Response

from api.v1.auth.dependencies.deps import get_obtain_token_use_case, get_logout_use_case
from api.v1.oauth2.dependencies.auth import get_user_or_401
from api.v1.oauth2.serializers.response.main import AccessTokenData
from core.auth.models import SessionORM
from core.auth.services import ObtainNewTokenPairUseCase
from core.auth.services import LogoutUseCase
from core.oauth.services import UserAPIKeyCredentials
from exceptions.db.auth import SessionNotFoundException
from utils.generics.dto import Result
from utils.generics.response import BadResponse, OkResponse


auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/refresh")
async def obtain_token(
    request: Request,
    response: Response,
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
    refresh_token: uuid.UUID = Cookie(...),
    service: ObtainNewTokenPairUseCase = Depends(get_obtain_token_use_case),
):
    result = await service.run(
        user=user,
        refresh_token=refresh_token,
        ip=request.client.host
    )
    match result:
        case Result(_, SessionNotFoundException() as err):
            return BadResponse.new(status_code=status.HTTP_404_NOT_FOUND, error=err.detail)
        case _:
            response.set_cookie(
                key="refresh_token",
                value=str(result[1].payload.refresh_token),
                expires=result[0].payload.expires_at.timestamp()
            )
            return OkResponse.new(payload=result[1].payload)


@auth.post("/logout")
async def logout(
    request: Request,
    response: Response,
    refresh_token: uuid.UUID = Cookie(...),
    service: LogoutUseCase = Depends(get_logout_use_case),
):
    await service.run(refresh_token=refresh_token)
    response.delete_cookie("refresh_token")
    return OkResponse.new(status_code=status.HTTP_204_NO_CONTENT, payload=None)
