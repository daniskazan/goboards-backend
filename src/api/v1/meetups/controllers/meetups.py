import uuid

from api.v1.meetups.serializers.request.main import GetMeetupListRequest, CreateMeetupRequest
from api.v1.meetups.serializers.response.main import GetMeetupListResponse
from api.v1.meetups.serializers.response.main import CreateMeetupResponse
from api.v1.oauth2.dependencies.auth import get_user_or_401
from api.v1.meetups.dependencies.deps import get_meetup_service
from core.oauth.services import UserAPIKeyCredentials
from core.meetups.services import MeetupService
from exceptions.db.meetups import MeetupNotFoundException

from fastapi import APIRouter, Depends, Request, status
from utils.generics.dto import Result
from utils.generics.response import BadResponse, OkResponse

meetups = APIRouter(prefix="/meetups", tags=["Meetups"])


@meetups.get("/", summary="Список текущих встреч", name="meetup:list")
async def get_meetup_list(
    request: Request,
    params: GetMeetupListRequest = Depends(),
    meetup_service: MeetupService = Depends(get_meetup_service),
    user: UserAPIKeyCredentials = Depends(get_user_or_401),
):
    result = await meetup_service.get_meetup_list(params=params)
    return OkResponse.new(payload=GetMeetupListResponse.get_meetup_list(result))


@meetups.get("/{meetup_id}", summary="Получить подробную информацию по встрече")
async def get_meetup_detail(
    request: Request,
    meetup_id: uuid.UUID,
    meetup_service: MeetupService = Depends(get_meetup_service),
    user: UserAPIKeyCredentials = Depends(get_user_or_401)
):
    result = await meetup_service.get_meetup_detail(meetup_id=meetup_id)
    match result:
        case Result(None, MeetupNotFoundException() as err):
            return BadResponse.new(status_code=status.HTTP_404_NOT_FOUND, error=err.detail)
        case Result(_, None):
            return OkResponse.new(payload=result.payload)


@meetups.post("/", summary="Создать встречу")
async def create_meetup(
    request: Request,
    body: CreateMeetupRequest,
    meetup_service: MeetupService = Depends(get_meetup_service),
):
    meetup = await meetup_service.create_meetup(params=body)
    r = CreateMeetupResponse.get_meetup(meetup)
    return OkResponse.new(status_code=status.HTTP_201_CREATED, payload=r)
