# 🚀 NexasPay API

> [!IMPORTANT]
> **API AINDA EM DESENVOLVIMENTO EM FASE DE TESTES!**

Bem-vindo à **NexasPay API**, o coração do nosso sistema de carteira digital inteligente. Esta API foi desenvolvida para oferecer uma plataforma robusta, segura e escalável para gerenciamento de usuários, carteiras e transações financeiras.

[](https://www.google.com/search?q=https://github.com/seu-usuario/nexaspay-api)
[](https://opensource.org/licenses/MIT)
[](https://www.python.org/downloads/release/python-311/)

## ✨ Visão Geral

A NexasPay API é uma solução de backend completa, construída com as mais modernas tecnologias Python, para fornecer serviços essenciais de uma carteira digital, incluindo:

  * **Autenticação de Usuários:** Cadastro e login seguros.
  * **Gerenciamento de Carteiras:** Criação e consulta de carteiras digitais.
  * **Transações Financeiras:** Realização de transferências, depósitos e pagamentos.
  * **Estrutura de Dados Abrangente:** Modelos para usuários, telefones, endereços e mais.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando um conjunto de tecnologias de ponta para garantir performance e manutenibilidade:

  * **FastAPI:** Framework web de alta performance para a construção de APIs.
  * **SQLAlchemy:** ORM (Mapeador Objeto-Relacional) para uma interação elegante e eficiente com o banco de dados.
  * **PostgreSQL:** Banco de dados relacional robusto e confiável.
  * **Docker & Docker Compose:** Para garantir um ambiente de desenvolvimento e produção consistente e de fácil configuração.
  * **Uvicorn:** Servidor ASGI (Asynchronous Server Gateway Interface) ultrarrápido.
  * **Pydantic:** Para validação de dados, garantindo a integridade e consistência das informações.
  * **Python 3.11:** Utilizando os recursos mais recentes da linguagem Python.

## ⚙️ Estrutura do Projeto

O projeto segue uma estrutura modular e organizada, visando a escalabilidade e a facilidade de manutenção:

```
/
|-- app/
|   |-- __init__.py           # Inicialização do módulo e carregamento de variáveis de ambiente
|   |-- main.py               # Ponto de entrada da aplicação FastAPI
|   |-- dependencies.py       # Dependências reutilizáveis da aplicação
|   |-- models.py             # Modelos de dados SQLAlchemy
|   |-- db/
|   |   |-- session.py        # Configuração da sessão do banco de dados
|   |-- enums/
|   |   |-- enums.py          # Enumerações utilizadas nos modelos
|   |-- routers/
|       |-- auth.py           # Rotas de autenticação
|       |-- transaction.py    # Rotas para transações
|       |-- wallet.py         # Rotas para carteiras
|-- tests/
|   |-- generate_id.py        # Script de teste para geração de IDs
|-- .gitignore                # Arquivos a serem ignorados pelo Git
|-- Dockerfile                # Instruções para a construção da imagem Docker
|-- docker-compose.yml        # Orquestração dos contêineres Docker
|-- README.md                 # Documentação do projeto
|-- requirements.txt          # Dependências Python do projeto
```

## 🚀 Começando

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento localmente.

### Pré-requisitos

  * [Docker](https://www.docker.com/get-started)
  * [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/nexaspay-api.git
    cd nexaspay-api
    ```

2.  **Crie e configure o arquivo `.env`:**
    Crie um arquivo chamado `.env` na raiz do projeto e preencha com as suas credenciais. Você pode usar o exemplo abaixo como base:

    ```env
    # Configurações do Banco de Dados
    DATABASE_URL=postgresql+asyncpg://seu_usuario:sua_senha@db:5432/seu_banco_de_dados
    POSTGRES_PASSWORD=sua_senha_segura

    # Chave Secreta para JWT
    SECRET_KEY=sua_chave_secreta_super_segura

    # Configurações da AWS (se aplicável)
    AWS_REGION=us-east-1
    ```

3.  **Inicie os serviços com Docker Compose:**

    ```bash
    docker-compose up --build
    ```

Após a conclusão, a API estará acessível em [`http://localhost:8000`](https://www.google.com/search?q=http://localhost:8000).

## 📚 Endpoints da API

A documentação interativa da API (gerada automaticamente pelo FastAPI) está disponível em:

  * **Swagger UI:** [`http://localhost:8000/docs`](https://www.google.com/search?q=http://localhost:8000/docs)
  * **ReDoc:** [`http://localhost:8000/redoc`](https://www.google.com/search?q=http://localhost:8000/redoc)

### Principais Rotas

#### Autenticação (`/auth`)

  * `POST /register`: Registra um novo usuário na plataforma.

#### Carteira (`/wallet`)

  * `GET /`: Retorna uma lista de todas as carteiras.
  * `GET /{owner_id}`: Retorna as carteiras de um usuário específico.
  * `POST /create`: Cria uma nova carteira.

#### Transação (`/transaction`)

  * `GET /`: Retorna uma lista de todas as transações.
  * `POST /create`: Cria uma nova transação entre duas carteiras.

-----

