from typing import List
import strawberry


@strawberry.type
class CidadeField:
    name: str
    value: str


@strawberry.type
class Cidade:
    id: strawberry.ID
    fields: List[CidadeField]
