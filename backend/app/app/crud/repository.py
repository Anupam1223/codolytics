from typing import Any, Dict, Optional, Union, Sequence, Awaitable, List

from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session

from ..deps import get_db
from ..crud.base import CRUDBase
from ..models.repository import Repository
from ..schemas.repository import RepositoryCreate, RepositoryUpdate


class CRUDRepository(CRUDBase[Repository, RepositoryCreate, RepositoryUpdate]):
    def create_repository(self, *, obj_in: RepositoryCreate) -> Repository:
        db = next(get_db())
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(name=obj_in_data["name"], project_id=obj_in_data["project"])
        db.add(db_obj)
        db.commit()
        # db.refresh_db(db_obj)
        return db_obj

    def get_repositories(self) -> List[Repository]:
        db = next(get_db())
        return db.query(Repository).all()

    def get_repository_by_id(self, db: Session, *, id):
        return db.query(Repository).filter(Repository.id == id).all()

    def get_repository_by_project_id(self, *, project_id):
        db = next(get_db())
        return db.query(Repository).filter(Repository.project_id == project_id).all()


repository = CRUDRepository(Repository)
