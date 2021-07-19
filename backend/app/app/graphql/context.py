from typing import Any, Dict

from sqlalchemy.orm import Session
from starlette.requests import Request

GraphQLContext = Dict[str, Any]


async def get_graphql_context(request: Request, db: Session) -> GraphQLContext:
    return {"request": request, "db": db}
