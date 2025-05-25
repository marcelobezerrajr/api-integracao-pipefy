import strawberry
from app.api.resolvers import create_card, delete_card, advance_phase


@strawberry.type
class Mutation:
    create_card: str = strawberry.mutation(resolver=create_card)
    delete_card: str = strawberry.mutation(resolver=delete_card)
    advance_phase: str = strawberry.mutation(resolver=advance_phase)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Bem-vindo à API GraphQL de integração com Pipefy"


schema = strawberry.Schema(query=Query, mutation=Mutation)
