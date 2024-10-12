import uuid

from dataclasses import dataclass

from core.users.models import UserORM
from core.users.repository.db.read_repo import UserReadRepository
from exceptions.db.users import UserNotFoundException
from utils.generics.dto import Result


@dataclass(kw_only=True)
class UserService:
    user_read_repo: UserReadRepository

    async def get_user_detail(self, *, user_id: uuid.UUID) -> Result[UserORM, None] | Result[None, UserNotFoundException]:
        return await self.user_read_repo.get_user_detail(user_id=user_id)
