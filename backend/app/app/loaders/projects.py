from typing import Awaitable, Optional, Sequence, Union

from ..crud import crud_project
from ..graphql import GraphQLContext
from ..models.project import Project
from .loader import get_loader


def load_project(
    context: GraphQLContext, project_id: Union[int, str]
) -> Awaitable[Optional[Project]]:
    loader = get_loader(context, "project", crud_project.get_project_by_id)
    return loader.load(project_id)


def load_projects(
    context: GraphQLContext, ids: Sequence[int]
) -> Awaitable[Sequence[Optional[Project]]]:
    loader = get_loader(context, "project", crud_project.get_project_by_id)
    loader.load_many(ids)
