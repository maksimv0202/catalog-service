from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Building
from core.repositories.base import GenericRepository


class BuildingRepository(GenericRepository[Building]):

    def __init__(self, _session: AsyncSession):
        super().__init__(Building, _session)

    # New methods for this Repository
    # ...
