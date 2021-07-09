from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_project(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        obj_in_data = jsonable_encoder(obj_in)
        print("obj_in_data", obj_in_data)
        db_obj = self.model(
            name=obj_in_data["name"], owner_id=obj_in_data["owner"]["id"]
        )
        print("db_obj", db_obj)
        db.add(db_obj)
        db.commit()
        # db.refresh_db(db_obj)
        return db_obj

    def get_projects(self, db: Session) -> List[Project]:
        return db.query(Project).all()

    async def get_project_by_id(self, db: Session, *, ids):
        return db.query(Project).filter(Project.id.in_(ids)).all()


project = CRUDProject(Project)
