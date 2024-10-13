from fastapi import Query
from pydantic import Field, PositiveInt, StrictInt, field_validator

from utils.generics.response import PydanticBaseModel


class CreateGameRequest(PydanticBaseModel):
    name: str = Field(..., description="Название игры")

    @field_validator("name")
    def type_to_description(cls, v: str):  # noqa: N805
        return v.capitalize()


class GetGameListRequest(PydanticBaseModel):
    name: str | None = Field(None, description="Название игры")
    limit: PositiveInt = Field(default=Query(default=100))
    offset: StrictInt = Field(default=Query(default=0))
