import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from .activity import ActivityShortOut
from .building import BuildingShortOut


class OrganizationBase(BaseModel):
    name: Annotated[str, Field(..., max_length=255)]
    phone_number: Annotated[str, Field(..., max_length=255)]
    building_id: int
    activity_id: int


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Annotated[str | None, Field(..., max_length=255)] = None
    phone_number: Annotated[str | None, Field(..., max_length=255)] = None
    building_id: int | None = None
    activity_id: int | None = None


class OrganizationOut(BaseModel):
    id: int
    name: Annotated[str, Field(..., max_length=255)]
    phone_number: Annotated[str, Field(..., max_length=255)]
    building: BuildingShortOut
    activity: ActivityShortOut

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {'from_attributes': True}
