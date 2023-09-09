from typing import TYPE_CHECKING

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from .base import Base

if TYPE_CHECKING:
    from .contract import Contract

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    created: Mapped[str | None] = mapped_column(Date, default=date.today())

    contracts: Mapped[list['Contract']] = relationship(back_populates='project')

    def __str__(self):
        return f'Project(id={self.id!r}, title={self.title!r}, created={self.created!r})'

    def __repr__(self):
        return str(self)