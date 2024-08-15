from dataclasses import dataclass

from api.v1.areas.serializers.main import Area
from core.areas.repository.db.read_repo import AreaReadRepository
from utils.generics.dto import Result


@dataclass
class AreaService:
    area_read_repo: AreaReadRepository

    async def get_area_list(self) -> Result[list[Area], None]:
        return await self.area_read_repo.get_area_list()
