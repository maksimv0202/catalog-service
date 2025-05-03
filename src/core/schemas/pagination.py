from typing import Annotated

from pydantic import BaseModel, Field


class PageParams(BaseModel):
    page: Annotated[int, Field(default=1, ge=1)]
    limit: Annotated[int, Field(default=100, ge=1, le=100)]
