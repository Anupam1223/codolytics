from typing import Optional

from pydantic import BaseModel

from .repository import Repository


# Shared properties
class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive via API on creation
class ProjectCreate(ProjectBase):
    name: str
    owner: int


# Properties to receive via API on update
class ProjectUpdate(ProjectBase):
    id: int
    name: Optional[str] = None


class ProjectInDBBase(ProjectBase):
    id: int
    name: str
    description: str
    repository: Optional[Repository] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Project(ProjectInDBBase):
    pass


# Additional properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
