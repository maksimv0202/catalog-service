from collections.abc import Sequence

from geopy.distance import distance, geodesic

from core.models import Organization
from core.repositories.organization import OrganizationRepository


class OrganizationService:

    def __init__(self, repository: OrganizationRepository):
        self._repository = repository

    @staticmethod
    def _get_bound_box(lat: float, lon: float, radius: int) -> tuple[float, float, float, float]:
        origin = (lat, lon)
        return (
            distance(meters=radius).destination(origin, bearing=180).latitude,
            distance(meters=radius).destination(origin, bearing=0).latitude,
            distance(meters=radius).destination(origin, bearing=270).longitude,
            distance(meters=radius).destination(origin, bearing=90).longitude,
        )

    async def search_by_radius(self, lat: float, lon: float, radius: int,
                               limit: int = 100, offset: int = 0) -> Sequence[Organization]:
        min_lat, max_lat, min_lon, max_lon = self._get_bound_box(lat, lon, radius)
        candidates = await self._repository.filter(
            limit=limit,
            offset=offset,
            building__latitude__in=(min_lat, max_lat),
            building__longitude__in=(min_lon, max_lon)
        )
        return [organization
                for organization in candidates
                if geodesic((lat, lon),
                            (organization.building.latitude, organization.building.longitude)).meters <= radius]

    async def search_by_area(self, lat1: float, lon1: float, lat2: float, lon2: float,
                             limit: int = 100, offset: int = 0) -> Sequence[Organization]:
        min_lat, max_lat = sorted((lat1, lat2))
        min_lon, max_lon = sorted((lon1, lon2))
        return await self._repository.filter(
            limit=limit,
            offset=offset,
            building__latitude__in=(min_lat, max_lat),
            building__longitude__in=(min_lon, max_lon)
        )
