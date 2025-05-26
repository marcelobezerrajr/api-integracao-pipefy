from typing import List
import strawberry

from app.api.resolvers import create_card, delete_card, advance_phase, list_cards
from app.schemas.card_shema import Card


@strawberry.input
class CreateCardInput:
    pipe_id: int
    name: str
    email: str
    telefone: str


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Cria um novo card em um pipe")
    def create_card(self, input: CreateCardInput) -> str:
        return create_card(input.pipe_id, input.name, input.email, input.telefone)

    @strawberry.mutation(description="Deleta um card pelo ID")
    def delete_card(self, card_id: str) -> str:
        return delete_card(card_id)

    @strawberry.mutation(description="Avança o card para a próxima fase")
    def advance_phase(self, card_id: str) -> str:
        return advance_phase(card_id)


@strawberry.type
class Query:
    @strawberry.field(description="Mensagem de boas-vindas para teste")
    def hello(self) -> str:
        return "Bem-vindo à API GraphQL de integração com Pipefy"

    @strawberry.field(description="Lista os cards de um pipe")
    def list_cards(self, pipe_id: int) -> List[Card]:
        return list_cards(pipe_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
