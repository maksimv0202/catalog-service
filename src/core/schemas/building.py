import datetime

from pydantic import BaseModel, Field
from typing import Annotated


class BuildingBase(BaseModel):
    address: str
    latitude: Annotated[float, Field(ge=-90.0, le=90.0)]
    longitude: Annotated[float, Field(ge=-180.0, le=180.0)]


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: str | None = None
    latitude: Annotated[float | None, Field(ge=-90.0, le=90.0)] = None
    longitude: Annotated[float | None, Field(ge=-180.0, le=180.0)] = None


class BuildingOut(BuildingBase):
    id: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {'from_attributes': True}
