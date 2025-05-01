from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Activity(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('activity.id', ondelete='SET NULL'),
        nullable=True
    )
    children: Mapped['Activity | None'] = relationship(back_populates='parent')
    parent: Mapped[list['Activity']] = relationship(back_populates='children', remote_side=[id])

    def __repr__(self):
        return f'<{self.__class__.__name__}(id={self.id}, name={self.name}, parent_id={self.parent_id})>'

    def __str__(self):
        return self.__repr__()
