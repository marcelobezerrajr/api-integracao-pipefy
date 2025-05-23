import requests
from requests.exceptions import RequestException
from app.core.config import PIPEFY_API_URL, PIPEFY_TOKEN, PIPE_ID, FINAL_PHASE_ID


class PipefyService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PIPEFY_TOKEN}",
            "Content-Type": "application/json",
        }

    def execute(self, query: str, variables: dict = None):
        try:
            response = requests.post(
                PIPEFY_API_URL,
                json={"query": query, "variables": variables},
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            json_data = response.json()

            if "errors" in json_data:
                raise Exception(f"GraphQL error: {json_data['errors']}")

            return json_data
        except RequestException as e:
            raise Exception(f"Erro de rede ao acessar o Pipefy: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro geral ao executar requisição Pipefy: {str(e)}")

    def create_card(self, name: str, email: str, telefone: str) -> str:
        mutation = """
        mutation CreateCard($pipe_id: ID!, $fields_attributes: [FieldValueInput]) {
          createCard(input: {
            pipe_id: $pipe_id,
            fields_attributes: $fields_attributes
          }) {
            card { id }
          }
        }
        """
        fields = [
            {"field_id": "nome", "field_value": name},
            {"field_id": "email", "field_value": email},
            {"field_id": "telefone", "field_value": telefone},
        ]
        result = self.execute(
            mutation, {"pipe_id": PIPE_ID, "fields_attributes": fields}
        )
        return result["data"]["createCard"]["card"]["id"]

    def delete_card(self, card_id: str) -> str:
        mutation = """
        mutation DeleteCard($id: ID!) {
          deleteCard(input: {id: $id}) {
            success
          }
        }
        """
        result = self.execute(mutation, {"id": card_id})
        return f"Deletado: {result['data']['deleteCard']['success']}"

    def advance_card_phase(self, card_id: str) -> str:
        mutation = """
        mutation MoveCard($card_id: ID!, $destination_phase_id: ID!) {
          moveCardToPhase(input: {
            card_id: $card_id,
            destination_phase_id: $destination_phase_id
          }) {
            card { id }
          }
        }
        """
        result = self.execute(
            mutation, {"card_id": card_id, "destination_phase_id": FINAL_PHASE_ID}
        )
        return f"Card {card_id} movido para fase final. {result['data']["destination_phase_id"]['success']}"
