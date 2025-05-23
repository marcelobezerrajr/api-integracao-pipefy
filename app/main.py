from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from strawberry.fastapi import GraphQLRouter
from app.schemas.pipefy_schemas import schema

app = FastAPI(
    title="Integração Pipefy GraphQL API",
    description="API para integração com Pipefy para cadastro de Pessoa",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
