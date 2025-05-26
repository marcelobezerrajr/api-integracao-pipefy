from typing import List

from app.services.pipefy_service import PipefyService
from app.schemas.card_shema import Card

pipefy = PipefyService()


def create_card(pipe_id: int, name: str, email: str, telefone: str) -> str:
    return pipefy.create_card(pipe_id, name, email, telefone)


def delete_card(card_id: str) -> str:
    return pipefy.delete_card(card_id)


def advance_phase(card_id: str) -> str:
    return pipefy.advance_card_phase(card_id)


def list_cards(pipe_id: int) -> List[Card]:
    cards = pipefy.list_cards(pipe_id)
    return [
        Card(
            id=card["id"],
            title=card["title"],
            created_at=card["created_at"],
            current_phase=card["current_phase"]["name"],
            fields=[f"{field['name']}: {field['value']}" for field in card["fields"]],
        )
        for card in cards
    ]
