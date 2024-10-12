from fastapi import Depends

from core.users.repository.db.read_repo import UserReadRepository
from core.users.services import UserService
from utils.db.session import get_db


def get_user_read_repo(session=Depends(get_db)) -> UserReadRepository:
    return UserReadRepository(session=session)


def get_user_service(user_read_repo=Depends(get_user_read_repo)) -> UserService:
    return UserService(user_read_repo=user_read_repo)
