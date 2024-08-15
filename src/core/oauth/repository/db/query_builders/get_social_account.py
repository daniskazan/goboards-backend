from core.oauth.models import SocialAccountORM
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select


class GetSocialAccountQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def __select_banners(cls):
        cls.__result_query = select(SocialAccountORM)
        return cls

    @classmethod
    def __filter_by_provider(cls, *, provider: str):
        cls.__result_query = cls.__result_query.where(SocialAccountORM.provider == provider)
        return cls

    @classmethod
    def __filter_user_id(cls, *, user_id: int):
        cls.__result_query = cls.__result_query.where(
            SocialAccountORM.extra_data["user_id"] == user_id  # noqa
        )
        return cls

    @classmethod
    def __build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, provider: str, user_id: int) -> Select:
        q = cls.__select_banners().__filter_by_provider(provider=provider).__filter_user_id(user_id=user_id).__build()
        return q
