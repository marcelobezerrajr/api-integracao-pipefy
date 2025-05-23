from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello():
    response = client.post("/graphql", json={"query": "{ hello }"})
    assert response.status_code == 200
    assert (
        response.json()["data"]["hello"]
        == "Bem-vindo à API GraphQL de integração com Pipefy"
    )


# pytest test/test_api.py
