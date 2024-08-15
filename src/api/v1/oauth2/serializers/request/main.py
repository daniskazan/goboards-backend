from pydantic import Field
from utils.generics.response import PydanticBaseModel


class UserLoginVKRequest(PydanticBaseModel):
    code: str = Field(..., description="Код авторизации от ВКонтакте")
