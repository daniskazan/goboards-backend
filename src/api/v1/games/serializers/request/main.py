from fastapi import Query
from pydantic import Field, PositiveInt, StrictInt
from utils.generics.response import PydanticBaseModel


class CreateGameRequest(PydanticBaseModel):
    name: str = Field(..., description="Название игры")


class GetGameListRequest(PydanticBaseModel):
    name: str | None = Field(None, description="Название игры")
    limit: PositiveInt = Field(default=Query(default=100))
    offset: StrictInt = Field(default=Query(default=0))
