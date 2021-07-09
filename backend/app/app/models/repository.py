from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .project import Project  # noqa: F401


class Repository(Base):
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="repositories")
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean(), default=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<Repository {self.id} {self.name}>"
