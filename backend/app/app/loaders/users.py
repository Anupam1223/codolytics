from typing import Awaitable, Optional, Sequence, Union

from ..crud import user
from ..graphql import GraphQLContext
from ..models.user import User
from .loader import get_loader


def load_user(
    context: GraphQLContext, user_id: Union[int, str]
) -> Awaitable[Optional[User]]:
    loader = get_loader(context, "user", user.get_users_by_id)
    return loader.load(user_id)


def load_users(
    context: GraphQLContext, ids: Sequence[Union[int, str]]
) -> Awaitable[Sequence[Optional[User]]]:
    loader = get_loader(context, "user", user.get_users_by_id)
    return loader.load_many(ids)
