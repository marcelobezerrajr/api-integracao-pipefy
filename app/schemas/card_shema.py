from typing import List
import strawberry


@strawberry.type
class CardField:
    name: str
    value: str


@strawberry.type
class Card:
    id: strawberry.ID
    title: str
    created_at: str
    current_phase: str
    fields: List[CardField]


@strawberry.input
class CreateCardInput:
    pipe_id: int
    name: str
    email: str
    telefone: str
    cidade_id: int
