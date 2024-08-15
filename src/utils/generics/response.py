from typing import Annotated, Generic, Self, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, alias_generators

T = TypeVar("T")
Payload = TypeVar("Payload")
ErrorDescription = TypeVar("ErrorDescription")


class APIResponse(JSONResponse, Generic[Payload]):
    """
    когда будем возвращать клиенту OkResponse/BadResponse
    этот класс проставит статус ответа в у самого объекта респонса
    """

    def render(self, content: T) -> bytes:
        if "statusCode" in content:
            self.status_code = content["statusCode"]
        return super().render(content=content)


class PydanticBaseModel(BaseModel):
    """
    Base model for all API Responses
    """

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class OkResponse(PydanticBaseModel, Generic[Payload]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: Annotated[int, Field(strict=True, ge=0, le=299)]
    payload: T

    @classmethod
    def new(cls, *, status_code: int = 200, payload: Payload) -> Self:
        return cls(status_code=status_code, payload=payload)


class BadResponse(PydanticBaseModel, Generic[ErrorDescription]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status_code: Annotated[int, Field(strict=True, ge=400, le=499)]
    error: ErrorDescription

    @classmethod
    def new(cls, *, status_code: int = 400, error: ErrorDescription) -> Self:
        return cls(status_code=status_code, error=error)
