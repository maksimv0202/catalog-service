import datetime

from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}


metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
