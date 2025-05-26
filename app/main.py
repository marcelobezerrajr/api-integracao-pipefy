from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from strawberry.fastapi import GraphQLRouter
import logging

from app.schemas.pipefy_schema import schema

app = FastAPI(
    title="Integração Pipefy GraphQL API",
    description="API para integração com Pipefy para cadastro de Pessoa",
    version="1.0.0",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro interno em {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno do servidor. Tente novamente mais tarde."},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Erro de validação em {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
