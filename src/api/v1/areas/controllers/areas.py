from fastapi import APIRouter, Depends, Request

from api.v1.areas.dependencies.deps import get_area_service
from api.v1.areas.serializers.main import (
    GetAreaListResponse,
)
from api.v1.oauth2.dependencies.auth import get_user_or_401
from core.areas.services import AreaService
from core.oauth.services import UserAPIKeyCredentials
from utils.generics.response import OkResponse


areas = APIRouter(prefix="/areas", tags=["Areas"])


@areas.get("/")
async def get_areas(
    request: Request,
    area_service: AreaService = Depends(get_area_service),
    user: UserAPIKeyCredentials = Depends(get_user_or_401)
):
    result = await area_service.get_area_list()
    return OkResponse.new(payload=GetAreaListResponse.get_area_list(result))
