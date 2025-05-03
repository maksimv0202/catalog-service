import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from .activity import ActivityShortOut
from .building import BuildingShortOut


class OrganizationBase(BaseModel):
    name: Annotated[str, Field(..., max_length=255)]
    phone_number: Annotated[str, Field(..., max_length=255)]
    building_id: Annotated[int, Field(..., ge=1)]
    activity_id: Annotated[int, Field(..., ge=1)]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Annotated[str | None, Field(..., max_length=255)] = None
    phone_number: Annotated[str | None, Field(..., max_length=255)] = None
    building_id: Annotated[int | None, Field(..., ge=1)] = None
    activity_id: Annotated[int | None, Field(..., ge=1)] = None


class OrganizationOut(BaseModel):
    id: int
    name: Annotated[str, Field(..., max_length=255)]
    phone_number: Annotated[str, Field(..., max_length=255)]
    building: BuildingShortOut
    activity: ActivityShortOut

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {'from_attributes': True}
