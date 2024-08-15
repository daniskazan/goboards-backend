from fastapi import Depends

from core.areas.repository.db.read_repo import AreaReadRepository
from core.areas.services import AreaService
from utils.db.session import get_db


def get_area_repo(session=Depends(get_db)):
    return AreaReadRepository(session=session)


def get_area_service(area_read_repo=Depends(get_area_repo)) -> AreaService:
    return AreaService(area_read_repo=area_read_repo)
