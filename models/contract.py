from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from .base import Base


if TYPE_CHECKING:
    from .project import Project

class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    created: Mapped[str] = mapped_column(Date, default=date.today())
    signed: Mapped[str | None] = mapped_column(Date, nullable=True, default=None)
    status: Mapped[str | None] = mapped_column(String(30), default='Черновик')
    
    project_id: Mapped[int | None] = mapped_column(ForeignKey('projects.id'), nullable=True, default=None)
    project: Mapped['Project'] = relationship(back_populates='contracts')

    def __str__(self):
        return f'Contract(id={self.id!r}, title={self.title!r}, created={self.created!r})'

    def __repr__(self):
        return str(self)
    
    