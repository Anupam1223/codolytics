from typing import Any, Dict

from starlette.requests import Request
from sqlalchemy.orm import Session

GraphQLContext = Dict[str, Any]


async def get_graphql_context(request: Request, db: Session) -> GraphQLContext:
    return {"request": request, "db": db}
