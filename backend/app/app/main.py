from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware

# from starlette.datastructures import URL


from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session

from .graphql.context import get_graphql_context
from .api.api_v1.api import api_router
from .graphql import GraphQLContext
from .graphql.schema import schema
from .core.config import settings
from .deps import get_db


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def resolve_graphql_context(
    request: Request, db: Session = Depends(get_db)
) -> GraphQLContext:
    return await get_graphql_context(request, db)


# settings.debug should be used
graphql = GraphQL(schema, debug=True, context_value=resolve_graphql_context)

app.mount("/graphql/", graphql)

# @app.get("/graphiql")
# async def graphiql(request: Request):
#     request._url = URL("/graphql")
#     return await graphql.render_playground(request=request)


# @app.post("/graphql")
# async def graphql_post(request: Request, db: Session = Depends(get_db)):
#     # app.mount("/graphql/", graphql)
#     request.state.db = db
#     return await graphql.handle_http(request=request)


# app.include_router(api_router, prefix=settings.API_V1_STR)
