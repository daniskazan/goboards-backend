import uuid

from pydantic import Field

from utils.generics.response import PydanticBaseModel


class AccessTokenVKResponse(PydanticBaseModel):
    """
    Ответ от ВК в ответ на успешный запрос токена
    """

    access_token: str = Field(..., description="")
    expires_in: int = Field(..., description="")
    user_id: int = Field(..., description="")


class AccessTokenData(PydanticBaseModel):
    access_token: str
    refresh_token: uuid.UUID
