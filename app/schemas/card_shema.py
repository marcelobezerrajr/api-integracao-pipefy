from typing import List
import strawberry


@strawberry.type
class Card:
    id: strawberry.ID
    title: str
    created_at: str
    current_phase: str
    fields: List[str]
