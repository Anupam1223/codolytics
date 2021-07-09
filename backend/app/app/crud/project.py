from typing import Any, Dict, Optional, Union, Sequence, Awaitable, List

from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session

from ..deps import get_db
from ..crud.base import CRUDBase
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_project(self, *, obj_in: ProjectCreate) -> Project:
        db = next(get_db())
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(name=obj_in_data["name"], owner_id=obj_in_data["owner"])
        db.add(db_obj)
        db.commit()
        # db.refresh_db(db_obj)
        return db_obj

    def get_projects(self) -> List[Project]:
        db = next(get_db())
        return db.query(Project).all()

    async def get_project_by_id(self, *, ids):
        db = next(get_db())
        return db.query(Project).filter(Project.id.in_(ids)).all()


project = CRUDProject(Project)
