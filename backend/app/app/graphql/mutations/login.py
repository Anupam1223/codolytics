from pydantic import BaseModel, create_model, EmailStr
from typing import Type

from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ..errorhandler import error_handler
from .. import GraphQLContext
from ...errors import AllFieldsAreRequiredError, InvalidCredentialsError

login_mutation = MutationType()
LoginInputModel = Type[BaseModel]


@login_mutation.field("login")
@error_handler
async def resolve_login(_, info: GraphQLResolveInfo, *, email: str, password: str):
    email = str(email or "").strip()
    password = str(password or "")
    input_model = await create_input_model(info.context)
    print("input model", input_model)
    if not email or not password:
        raise AllFieldsAreRequiredError
    return {
        "token": "adfkhsdkfhsadk",
        "user": {"id": 1, email: "tushant@gmail.com", "fullName": "Tushant"},
    }
    # if not user:
    #     raise InvalidCredentialsError


async def create_input_model(context: GraphQLContext) -> LoginInputModel:
    return create_model(
        "LoginInputModel",
        email=(EmailStr, ...),
        password=(str, ...),
    )
