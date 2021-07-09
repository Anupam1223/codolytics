from typing import Dict, List, Tuple, Any

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ...validation import (
    validate_model,
    Validator,
    validate_data,
    ProjectExistsValidator,
    RepositoryNameExistsValidator,
)
from ..context import GraphQLContext
from ...errors import ErrorsList
from ..errorhandler import error_handler
from ...schemas import RepositoryCreate
from ...crud import crud_repository

add_repository_mutation = MutationType()


@add_repository_mutation.field("addRepository")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_add_repository(_, info: GraphQLResolveInfo, *, input: dict):
    input_model = RepositoryCreate(**input)
    cleaned_data, errors = validate_model(input_model, input)
    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "project": [ProjectExistsValidator(info.context)],
            "name": [RepositoryNameExistsValidator()],
        }
        cleaned_data, errors = await validate_input_data(
            info.context, validators, cleaned_data, errors
        )
    if errors:
        return {"errors": errors}
    repository = crud_repository.create_repository(
        info.context["db"], obj_in=cleaned_data
    )
    return {"repository": repository, "success": True}


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: Dict[str, Any],
    errors: ErrorsList,
) -> Tuple[Dict[str, Any], ErrorsList]:
    return await validate_data(data, validators, errors)
