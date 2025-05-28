<h1 align="center">Pipefy GraphQL API 🤖</h1>

API desenvolvida em Python com FastAPI e Strawberry para integração com a API GraphQL do Pipefy. Permite criar, listar, atualizar e deletar cards de forma robusta e automatizada.

## ⚙️ Tecnologias

- Python 3.11+
- FastAPI
- Strawberry GraphQL
- Uvicorn
- Pipefy GraphQL API

## 🧑🏻‍💻 Funcionalidades

### Mutations

#### `create_card`

Cria um novo card no pipe informado.

```graphql
mutation CreateCard {
  create_card(
    input: {
      pipe_id: 123456
      name: "João"
      email: "joao@email.com"
      telefone: "11999999999"
      cidade_id: 123456
    }
  )
}
```

#### `delete_card`

Deleta um card pelo seu ID.

```graphql
mutation DeleteCard {
  delete_card(card_id: 123456789)
}
```

#### `advance_phase`

Move o card automaticamente para a próxima fase do pipe.

```graphql
mutation AdvancePhase {
  advance_phase(card_id: 123456789)
}
```

### Queries

#### `hello`

Verifica se a API está ativa.

```graphql
query Hello {
  hello
}
```

#### `list_cards`

Retorna os cards do pipe, com fase atual, data e campos preenchidos.

```graphql
query ListCards {
  list_cards(pipe_id: 123456) {
    id
    title
    created_at
    current_phase
    fields {
      name
      value
    }
  }
}
```

#### `list_cidades`

Retorna as cidades da tabela do database do pipefy.

```graphql
query ListCidades {
  listCidades(tableId: 123456) {
    id
    fields {
      name
      value
    }
  }
}
```

## ▶️ Instalação e Execução

```bash
# Clone o projeto
$ git clone ...
$ cd api-integracao-pipefy

# Crie e ative o ambiente virtual
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate    # Windows

# Instale as dependências
$ pip install -r requirements.txt

# Rode a API localmente
$ uvicorn app.main:app --reload
```

Acesse a interface GraphQL em: http://localhost:8000/graphql

## 🔐 .env (exemplo)

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```graphql
PIPEFY_API_URL=url_da_api_aqui
PIPEFY_TOKEN=seu_token_aqui
```

## 📬 Testes (via Postman ou Playground)

Você pode testar os endpoints GraphQL usando o Postman ou o Playground, utilizando o seguinte endpoint:

```bash
http://localhost:8000/graphql
```

## 🔗 Collection no Postman

Uma collection pronta para testes está disponível no link abaixo:

👉 [Acessar collection no Postman](https://www.postman.com/marcelo-7952/integrao-pipefy-testes-de-api/collection/6830c0595ac051812a6b4c10?action=share&creator=39796403)
