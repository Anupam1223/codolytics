from typing import Union

from pydantic import PydanticValueError

from .autherror import AuthError
from .errordict import ErrorDict
from .errorslist import ErrorsList
from .format import get_error_dict, get_error_type


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class NotAuthorizedError(AuthError):
    code = "not_authorized"
    msg_template = "authorization is required"


class NotAdminError(AuthError):
    code = "not_admin"
    msg_template = "administrator permission is required"


class EmailNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class InvalidCredentialsError(PydanticValueError):
    code = "invalid_credentials"
    msg_template = "invalid credentials"


class NotProjectOwnerError(AuthError):
    code = "project.owner"
    msg_template = "must be owner of project with id '{id}'"

    def __init__(self, *, owner_id: Union[int, str]) -> None:
        super().__init__(id=owner_id)


class ProjectDoesNotExistError(PydanticValueError):
    code = "project.not_exists"
    msg_template = "project with id '{id}' does not exist"

    def __init__(self, *, project_id: Union[int, str]) -> None:
        super().__init__(id=project_id)


class ProjectExistsError(PydanticValueError):
    code = "project.already_exists"
    msg_template = "project with id '{id}' already exist"

    def __init__(self, *, project_id: Union[int, str]) -> None:
        super().__init__(id=project_id)


class ProjectNameExistError(PydanticValueError):
    code = "project.name_exists"
    msg_template = "project with name '{name}' already exist"

    def __init__(self, *, name: str) -> None:
        super().__init__(name=name)


class RepositoryDoesNotExistError(PydanticValueError):
    code = "repository.not_exists"
    msg_template = "repository with id '{id}' does not exist"

    def __init__(self, *, repository_id: Union[int, str]) -> None:
        super().__init__(id=repository_id)


class RepositoryNameExistError(PydanticValueError):
    code = "repository.name_exists"
    msg_template = "repository with name '{name}' already exist"

    def __init__(self, *, name: str) -> None:
        super().__init__(name=name)


class UserDoesNotExistError(PydanticValueError):
    code = "user.not_exists"
    msg_template = "user with id '{id}' does not exist"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)


class UsernameError(PydanticValueError):
    code = "username"
    msg_template = 'username does not match regex "{pattern}"'

    def __init__(  # pylint: disable=useless-super-delegation
        self, *, pattern: str
    ) -> None:
        super().__init__(pattern=pattern)


class UsernameNotAvailableError(PydanticValueError):
    code = "username.not_available"
    msg_template = "username is not available"


class UsernameNotAllowedError(PydanticValueError):
    code = "username.not_allowed"
    msg_template = "username is not allowed"
