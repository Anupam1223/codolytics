from typing import Dict, List, Tuple, Type, Any
from pydantic import create_model, BaseModel

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ...validation import (
    validate_model,
    Validator,
    UserExistsValidator,
    ProjectNameExistsValidator,
    validate_data,
)
from ...errors import ErrorsList
from ..errorhandler import error_handler
from ...crud import crud_project
from .. import GraphQLContext

add_project_mutation = MutationType()


@add_project_mutation.field("addProject")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_add_project(_, info: GraphQLResolveInfo, *, input: dict):
    input_model = await create_input_model(info.context)
    # data types validation
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
    project = crud_project.create_project(obj_in=cleaned_data)
    return {"project": project}


AddProjectInputModel = Type[BaseModel]


async def create_input_model(context: GraphQLContext) -> AddProjectInputModel:
    return create_model("AddProjectInputModel", owner=(int, ...), name=(str, ...))


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: Dict[str, Any],
    errors: ErrorsList,
) -> Tuple[Dict[str, Any], ErrorsList]:
    return await validate_data(data, validators, errors)
