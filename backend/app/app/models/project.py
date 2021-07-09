from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Project(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="projects")
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    is_active = Column(Boolean(), default=True)
    repositories = relationship("Repository", back_populates="project")
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<Project {self.id} {self.name}>"
