from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, exists
from sqlalchemy.orm import selectinload


from core.areas.models import AreaORM
from utils.generics.dto import Result


class AreaReadRepository:
    def __init__(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_area_list(self):
        q = text("select * from areas a where not exists(select 1 from areas sub where sub.parent_id = a.id)")
        result = await self._session.execute(q)
        return Result.success(payload=[row._mapping for row in result])
