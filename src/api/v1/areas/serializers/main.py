import uuid
from pydantic import Field
from typing import TypedDict
from core.areas.models import AreaORM
from utils.generics.dto import Result
from utils.generics.response import PydanticBaseModel


class Area(TypedDict):
    id: uuid.UUID
    name: str


class GetCityListRequest(PydanticBaseModel):
    name: str | None = Field(default=None)


class GetAreaListResponse(PydanticBaseModel):
    id: uuid.UUID = Field(alias="area_id")
    name: str

    @classmethod
    def get_area_list(cls, /, result: Result[list[Area], None]):
        return [cls.model_validate(c) for c in result.payload]
