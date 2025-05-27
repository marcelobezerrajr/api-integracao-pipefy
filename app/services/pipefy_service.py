from typing import Optional, Dict, Any, List
from requests.exceptions import RequestException
import requests

from app.core.config import PIPEFY_API_URL, PIPEFY_TOKEN


class PipefyService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PIPEFY_TOKEN}",
            "Content-Type": "application/json",
        }

    def execute(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                PIPEFY_API_URL,
                json={"query": query, "variables": variables},
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                message = "; ".join(
                    error.get("message", "Erro desconhecido")
                    for error in data["errors"]
                )
                raise Exception(f"Erro GraphQL: {message}")

            return data
        except RequestException as e:
            raise Exception(f"Erro de rede ao acessar o Pipefy: {str(e)}")
        except ValueError:
            raise Exception("Resposta inválida ao decodificar JSON.")
        except Exception as e:
            raise Exception(f"Erro geral ao executar requisição Pipefy: {str(e)}")

    def list_cards(self, pipe_id: int) -> List[Dict[str, Any]]:
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
        return [edge["node"] for edge in result["data"]["cards"]["edges"]]

    def list_cidades(self, table_id: int) -> List[Dict[str, Any]]:
        query = """
        query ListCidades($table_id: ID!) {
          table_records(table_id: $table_id, first: 100) {
            edges {
              node {
                id
                record_fields {
                  name
                  value
                }
              }
            }
          }
        }
        """
        result = self.execute(query, {"table_id": table_id})
        cidades = []

        for edge in result["data"]["table_records"]["edges"]:
            node = edge["node"]
            cidade_nome = next(
                (f["value"] for f in node["record_fields"] if f["name"] == "Nome"), ""
            )
            cidades.append({"id": int(node["id"]), "nome": cidade_nome})

        return cidades

    def create_card(
        self, pipe_id: int, name: str, email: str, telefone: str, cidade_id: int
    ) -> str:
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
            {"field_id": "cidade", "field_value": cidade_id},
        ]
        result = self.execute(
            mutation, {"pipe_id": pipe_id, "fields_attributes": fields}
        )
        return result["data"]["createCard"]["card"]["id"]

    def delete_card(self, card_id: int) -> str:
        mutation = """
          mutation DeleteCard($id: ID!) {
            deleteCard(input: {id: $id}) {
              success
            }
          }
        """
        result = self.execute(mutation, {"id": card_id})
        success = result["data"]["deleteCard"]["success"]
        return "Card deletado com sucesso." if success else "Falha ao deletar card."

    def advance_card_phase(self, card_id: int) -> str:
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
