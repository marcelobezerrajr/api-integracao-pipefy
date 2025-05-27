from typing import List, Dict
from strawberry.exceptions import GraphQLError

from app.services.pipefy_service import PipefyService
from app.schemas.card_shema import Card, Field

pipefy = PipefyService()


def list_cards(pipe_id: int) -> List[Card]:
    try:
        cards = pipefy.list_cards(pipe_id)
        return [
            Card(
                id=card["id"],
                title=card["title"],
                created_at=card["created_at"],
                current_phase=card["current_phase"]["name"],
                fields=[
                    Field(name=f["name"], value=f["value"]) for f in card["fields"]
                ],
            )
            for card in cards
        ]
    except Exception as e:
        raise GraphQLError(f"Erro ao listar cards: {str(e)}")


def list_cidades(table_id: int) -> List[Dict[str, str]]:
    try:
        return pipefy.list_cidades(table_id)
    except Exception as e:
        raise GraphQLError(f"Erro ao listar cidades: {str(e)}")


def create_card(
    pipe_id: int, name: str, email: str, telefone: str, cidade_id: int
) -> str:
    try:
        return pipefy.create_card(pipe_id, name, email, telefone, cidade_id)
    except Exception as e:
        raise GraphQLError(f"Erro ao criar card: {str(e)}")


def delete_card(card_id: int) -> str:
    try:
        return pipefy.delete_card(card_id)
    except Exception as e:
        raise GraphQLError(f"Erro ao deletar card: {str(e)}")


def advance_phase(card_id: int) -> str:
    try:
        return pipefy.advance_card_phase(card_id)
    except Exception as e:
        raise GraphQLError(f"Erro ao avançar fase do card: {str(e)}")
