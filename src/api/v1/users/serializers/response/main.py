import datetime as dt
import uuid

from pydantic import Field

from core.users.models import UserORM
from utils.generics.dto import Result
from utils.generics.response import PydanticBaseModel


class GetUserDetailResponse(PydanticBaseModel):
    class SocialLinks(PydanticBaseModel):
        provider: str = Field(alias="providerName")
        profile_url: str

    id: uuid.UUID = Field()
    username: str
    created_at: dt.datetime
    social_accounts: list[SocialLinks] = Field(alias="socialLinks")

    @classmethod
    def get_user_detail_info(cls, /, result: Result[UserORM, None]):
        return cls.model_validate(result.payload)
