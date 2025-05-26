from requests.exceptions import RequestException
import requests

from app.core.config import PIPEFY_API_URL, PIPEFY_TOKEN


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

    def create_card(self, pipe_id: int, name: str, email: str, telefone: str) -> str:
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
            mutation, {"pipe_id": pipe_id, "fields_attributes": fields}
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
        query = """
          query GetCard($id: ID!) {
            card(id: $id) {
              current_phase { id name }
              pipe { phases { id name } }
            }
          }
        """
        card_data = self.execute(query, {"id": card_id})["data"]["card"]
        current_phase = card_data.get("current_phase")
        all_phases = card_data.get("pipe", {}).get("phases", [])

        current_index = next(
            (
                i
                for i, phase in enumerate(all_phases)
                if phase["id"] == current_phase["id"]
            ),
            None,
        )

        if current_index is None or current_index + 1 >= len(all_phases):
            return f"Card {card_id} já está na fase final: {current_phase['name']}"

        next_phase = all_phases[current_index + 1]

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
        self.execute(
            mutation, {"card_id": card_id, "destination_phase_id": next_phase["id"]}
        )
        return f"Card {card_id} movido para a fase: {next_phase['name']}"

    def list_cards(self, pipe_id: int) -> list:
        query = """
          query GetCards($pipe_id: ID!) {
            cards(pipe_id: $pipe_id, first: 50) {
              edges {
                node {
                  id
                  title
                  created_at
                  current_phase {
                    name
                  }
                  fields {
                    name
                    value
                  }
                }
              }
            }
          }
        """
        result = self.execute(query, {"pipe_id": pipe_id})
        cards = result["data"]["cards"]["edges"]
        return [edge["node"] for edge in cards]
