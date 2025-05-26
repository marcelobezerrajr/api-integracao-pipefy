from typing import List
import strawberry

from app.api.resolvers import create_card, delete_card, advance_phase, list_cards
from app.schemas.card_shema import Card


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

    list_cards: List[Card] = strawberry.field(resolver=list_cards)


schema = strawberry.Schema(query=Query, mutation=Mutation)
