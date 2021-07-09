from typing import Optional

from pydantic import BaseModel


# Shared properties
class RepositoryBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class RepositoryCreate(RepositoryBase):
    name: str
    project: int


# Properties to receive via API on update
class RepositoryUpdate(RepositoryBase):
    id: int
    name: Optional[str] = None


class RepositoryInDBBase(RepositoryBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Repository(RepositoryInDBBase):
    pass


# Additional properties stored in DB
class RepositoryInDB(RepositoryInDBBase):
    pass
