from api.routes.building import router as building_router
from api.routes.activity import router as activity_router
from api.routes.organization import router as organization_router


__all__ = (
    'activity_router',
    'building_router',
    'organization_router'
)
