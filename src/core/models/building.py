from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Building(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return (f'<{self.__class__.__name__}(id={self.id}, address={self.address}, '
                f'coordinates=({self.latitude}, {self.longitude}))>')

    def __str__(self):
        return self.__repr__()
