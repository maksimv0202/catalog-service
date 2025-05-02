import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    name: str


class ActivityCreate(ActivityBase):
    parent_id: Annotated[int | None, Field(default=None)] = None

    model_config = {'from_attributes': True}


class ActivityOut(ActivityBase):
    id: int
    parent_id: int | None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {'from_attributes': True}


class ActivityWithChildrenOut(ActivityOut):
    children: list['ActivityOut'] = Field(default_factory=list)


class ActivityUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None
