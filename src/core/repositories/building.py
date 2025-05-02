from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Building
from core.repositories.base import GenericRepository


class BuildingRepository(GenericRepository[Building]):

    def __init__(self, session: AsyncSession):
        super().__init__(Building, session)

    # New methods for this Repository
    # ...
