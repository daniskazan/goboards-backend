import datetime as dt
from uuid import UUID

from core.games.enums import GameType
from core.games.models import GameORM
from pydantic import Field, field_validator
from utils.generics.dto import Result
from utils.generics.response import PydanticBaseModel


#  alias - те поля, которые отдаются фронтенду
class CreateGameResponse(PydanticBaseModel):
    """
    Ответ после добавления игры
    """

    game_id: UUID = Field(..., alias="id", description="Идентификатор игры")
    game_name: str = Field(..., alias="name", description="Название игры")
    type: GameType = Field(..., alias="game_type", description="Тип игры")

    @field_validator("type")
    def type_to_description(cls, v: GameType):
        return v.get_description()


class GetGameDetailResponse(PydanticBaseModel):
    id: UUID = Field(..., alias="game_id", description="Идентификатор игры")
    game_name: str = Field(..., alias="name", description="Название игры")
    type: GameType = Field(..., alias="game_type", description="Тип игры")
    created_at: dt.datetime = Field(..., description="Дата создания")

    @field_validator("type")
    def type_to_description(cls, v: GameType):
        return v.get_description()

    @classmethod
    def get_detail_info(cls, *, dto: Result[GameORM, None]):
        return cls.model_validate(dto.payload)


class GetGameListResponse(PydanticBaseModel):
    id: UUID = Field(..., alias="game_id", description="Идентификатор игры")
    name: str = Field(..., alias="game_name", description="Название игры")

    @classmethod
    def list_of_games(cls, *, dto: Result[list[GameORM], None]):
        return [cls.model_validate(game) for game in dto.payload]


class NestedGameMeetupListResponse(GetGameListResponse):
    pass
