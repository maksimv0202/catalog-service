from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Organization, Activity
from core.repositories.base import GenericRepository


class OrganizationRepository(GenericRepository[Organization]):

    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)

    async def search_by_activity_name(self, name: str) -> Sequence[Organization]:
        subtree = (
            select(Activity.id)
            .where(Activity.name == name)
            .cte(name='subtree', recursive=True)
        )
        subtree = subtree.union_all(
            select(Activity.id)
            .where(Activity.parent_id == subtree.c.id)
        )
        return (await self._session.execute(
            select(Organization)
            .where(Organization.activity_id.in_(select(subtree.c.id)))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activity)
            )
        )).scalars().all()
