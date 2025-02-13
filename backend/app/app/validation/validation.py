from asyncio import gather
from inspect import isawaitable
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

from pydantic import BaseModel, PydanticTypeError, PydanticValueError
from pydantic import validate_model as pydantic_validate_model

from ..errors import AuthError, ErrorsList

ROOT_LOCATION = ErrorsList.ROOT_LOCATION


Data = Dict[str, Any]

Validator = Callable[[Any, ErrorsList, str], Union[Awaitable[Any], Any]]


def validate_model(model: Type[BaseModel], input_data: Data) -> Tuple[Data, ErrorsList]:
    """Wrapper for pydantic.validate_model that always returns list for errors."""
    validated_data, _, errors = pydantic_validate_model(model, input_data)
    if not errors:
        return validated_data, ErrorsList()
    return validated_data, ErrorsList(cast(ErrorsList, errors.errors()))


async def validate_data(
    data: Data,
    validators: Dict[str, List[Validator]],
    errors: ErrorsList,
) -> Tuple[Data, ErrorsList]:
    if not data or not validators:
        return data, errors

    new_errors = errors.copy()

    validated_data: Data = {}

    validators_queue = []
    validators_queue_fields = []
    for field_name, field_data in data.items():
        if validators.get(field_name) and field_data is not None:
            field_validators = validators[field_name]
            validators_queue_fields.append(field_name)
            validators_queue.append(
                validate_field_data(
                    field_name, field_data, field_validators, new_errors
                )
            )
        else:
            validated_data[field_name] = field_data
    if validators_queue:
        for i, validated_field_data in enumerate(await gather(*validators_queue)):
            validated_field_name = validators_queue_fields[i]
            if validated_field_data is not None:
                validated_data[validated_field_name] = validated_field_data

    if ROOT_LOCATION in validators:
        for root_validator in validators[ROOT_LOCATION]:
            try:
                result = root_validator(validated_data, new_errors, ROOT_LOCATION)
                if isawaitable(result):
                    validated_data = cast(Data, await result)
                else:
                    validated_data = cast(Data, result)
            except (AuthError, PydanticTypeError, PydanticValueError) as error:
                new_errors.add_root_error(error)

    return validated_data, new_errors


async def validate_field_data(
    field_name: str,
    data: Any,
    validators: List[Validator],
    errors: ErrorsList,
) -> Optional[Any]:
    try:
        for validator in validators:
            data = validator(data, errors, field_name)
            if isawaitable(data):
                data = await (data)
        return data
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_error(field_name, error)
        return None
