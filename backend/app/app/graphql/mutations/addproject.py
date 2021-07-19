from typing import Any, Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ...crud import crud_project
from ...errors import ErrorsList
from ...schemas import ProjectCreate
from ...validation import (
    ProjectNameExistsValidator,
    UserExistsValidator,
    Validator,
    validate_data,
    validate_model,
)
from .. import GraphQLContext
from ..errorhandler import error_handler

add_project_mutation = MutationType()


@add_project_mutation.field("addProject")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_add_project(_, info: GraphQLResolveInfo, *, input: dict):
    # data types validation
    input_model = ProjectCreate(**input)
    cleaned_data, errors = validate_model(input_model, input)
    # database level validation
    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "owner": [UserExistsValidator(info.context)],
            "name": [ProjectNameExistsValidator()],
        }
        cleaned_data, errors = await validate_input_data(
            info.context, validators, cleaned_data, errors
        )
    if errors:
        return {
            "errors": errors,
        }
    print("cleaned data", cleaned_data)
    project = crud_project.create_project(info.context["db"], obj_in=cleaned_data)
    return {"project": project}


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: Dict[str, Any],
    errors: ErrorsList,
) -> Tuple[Dict[str, Any], ErrorsList]:
    return await validate_data(data, validators, errors)
