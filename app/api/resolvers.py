from app.services.pipefy_service import PipefyService

pipefy = PipefyService()


def create_card(pipe_id: int, name: str, email: str, telefone: str) -> str:
    return pipefy.create_card(pipe_id, name, email, telefone)


def delete_card(card_id: str) -> str:
    return pipefy.delete_card(card_id)


def advance_phase(card_id: str) -> str:
    return pipefy.advance_card_phase(card_id)
