from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.repository import Repository
from ..schemas.repository import RepositoryCreate, RepositoryUpdate


class CRUDRepository(CRUDBase[Repository, RepositoryCreate, RepositoryUpdate]):
    def create_repository(self, db: Session, *, obj_in: RepositoryCreate) -> Repository:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(name=obj_in_data["name"], project_id=obj_in_data["project"])
        db.add(db_obj)
        db.commit()
        # db.refresh_db(db_obj)
        return db_obj

    def get_repositories(self, db: Session) -> List[Repository]:
        return db.query(Repository).all()

    def get_repository_by_id(self, db: Session, *, ids):
        return db.query(Repository).filter(Repository.id.in_(ids)).all()

    def get_repository_by_project_id(self, db: Session, *, project_id):
        return db.query(Repository).filter(Repository.project_id == project_id).all()


repository = CRUDRepository(Repository)
