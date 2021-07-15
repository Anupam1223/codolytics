from typing import Awaitable, List, Optional

from ariadne import QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ...models.user import User
from ...models.project import Project
from ...models.repository import Repository
from ...crud import crud_project, crud_repository

query_type = QueryType()


@query_type.field("auth")
def resolve_auth(_, info: GraphQLResolveInfo) -> Awaitable[Optional[User]]:
    pass


@query_type.field("projects")
def resolve_projects(_, info: GraphQLResolveInfo) -> Awaitable[Optional[Project]]:
    return crud_project.get_projects(info.context["db"])


@query_type.field("repositories")
@convert_kwargs_to_snake_case
def resolve_repositories(
    _, info: GraphQLResolveInfo, *, project_id: Optional[List[str]] = None
) -> Awaitable[Optional[Repository]]:
    if project_id:
        return crud_repository.get_repository_by_project_id(
            info.context["db"], project_id=project_id
        )
    return crud_repository.get_repositories(info.context["db"])
