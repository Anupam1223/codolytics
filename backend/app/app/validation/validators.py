from typing import Any, Awaitable, Callable, Union

from ..deps import get_db
from ..errors import (
    ErrorsList,
    ProjectDoesNotExistError,
    ProjectExistsError,
    ProjectNameExistError,
    RepositoryNameExistError,
    UserDoesNotExistError,
)
from ..graphql import GraphQLContext
from ..loaders import load_project, load_user
from ..models.project import Project
from ..models.repository import Repository

Validator = Callable[[Any, ErrorsList, str], Union[Awaitable[Any], Any]]


class UserExistsValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, user_id: Union[int, str], *_) -> Any:
        user = await load_user(self._context, user_id)
        if not user:
            raise UserDoesNotExistError(user_id=user_id)
        return user


class ProjectDoesNotExistsValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext) -> None:
        self._context = context

    async def __call__(self, id: Union[int, str], *_) -> Any:
        project = await load_project(self._context, id)
        if not project:
            raise ProjectDoesNotExistError(project_id=id)
        return project


class ProjectExistsValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext) -> None:
        self._context = context

    async def __call__(self, id: Union[int, str], *_) -> Any:
        project = await load_project(self._context, id)
        if project:
            raise ProjectExistsError(project_id=id)
        return project


class ProjectNameExistsValidator:
    async def __call__(self, name: str, *_) -> Any:
        db = next(get_db())
        project = db.query(Project).filter(Project.name == name).first()
        if project:
            raise ProjectNameExistError(name=name)
        return name


class RepositoryNameExistsValidator:
    async def __call__(self, name: str, *_) -> Any:
        db = next(get_db())
        repository = db.query(Repository).filter(Repository.name == name).first()
        if repository:
            raise RepositoryNameExistError(name=name)
        return name
