from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .activity import Activity
from .base import Base
from .building import Building


class Organization(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    building_id: Mapped[int] = mapped_column(ForeignKey('building.id'), nullable=False)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'), nullable=False)

    building: Mapped['Building'] = relationship(back_populates='organizations', lazy='selectin')
    activity: Mapped['Activity'] = relationship(lazy='selectin')

    def __repr__(self):
        return (f'<{self.__class__.__name__}(id={self.id}, name={self.name}), '
                f'phone_number={self.phone_number}, activity_id={self.activity_id}, '
                f'building_id={self.building_id}>')

    def __str__(self):
        return self.__repr__()
