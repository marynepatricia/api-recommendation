# 📍 API de Recomendação de Lugares

Esta é uma API desenvolvida com FastAPI que utiliza a Google Places API para sugerir locais (restaurantes, museus, etc.) com base numa localização. O projeto utiliza PostgreSQL para cache de pesquisas e Docker para facilitar o ambiente de desenvolvimento.

## 🚀 Funcionalidades

* **Busca de Lugares:** Consulta a API do Google para obter nomes, moradas, classificações e tipos de locais.
* **Health Check:** Endpoint para verificar se a API está online.
* **Arquitetura Limpa:** Separação clara entre rotas, esquemas de dados (Pydantic) e serviços externos.
* **Testes Automatizados:** Suite de testes com mocks para simular a API do Google sem gastar créditos.

## 🚀 Novas Funcionalidades
* **Cache Inteligente:** Grava os resultados no banco de dados para evitar chamadas repetidas à API do Google, poupando créditos.
* **Gestão com UV:** Utiliza o gestor de pacotes uv para instalações ultra-rápidas.
* **Dual Mode:** Suporte total para execução via Docker ou Localmente.
* **Busca Normalizada:** Lógica que ignora acentos e preposições para garantir que "Restaurantes em Porto" e "restaurantes no porto" usem a mesma cache.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI:** Framework web de alta performance.
* **Uvicorn:** Servidor ASGI para correr a aplicação.
* **HTTPX:** Cliente HTTP assíncrono para comunicar com o Google.
* **UV:** Gestor de pacotes e ambientes Python extremamente rápido.
* **Docker:** Para facilitar a implementação em qualquer ambiente.

## 📂 Estrutura do Projeto

```├── app/
│   ├── core/
│   │   └── config.py      # Gestão de variáveis de ambiente e chaves API
│   ├── database/
│   │   ├── database.py    # Configuração da conexão assíncrona com PostgreSQL
│   │   └── models.py      # Definição das tabelas do banco de dados (SQLAlchemy)
│   ├── schemas/
│   │   └── schemas.py     # Modelos de validação de dados (Pydantic)
│   ├── services/
│   │   └── services.py    # Lógica de negócio e integração com Google Places
│   ├── main.py            # Ponto de entrada da API e definição de rotas
│   └── __init__.py
├── tests/
│   ├── test_main.py           # Testes de integração dos endpoints (com mocks)
│   └── test_bd_integration.py # Testes de fluxo de gravação na base de dados
├── Dockerfile                 # Configuração da imagem Docker otimizada com 'uv'
├── docker-compose.yml         # Orquestração da API e da base de dados Postgres
├── Makefile                   # Atalhos para comandos de desenvolvimento (Local/Docker)
├── pyproject.toml             # Definição de dependências e metadados do projeto
└── .env.example               # Modelo do arquivo .env
```

## ⚙️ Configuração Inicial

1. Pré-requisitos
* Python 3.12+: Versão base utilizada no projeto.
* UV: Gestor de pacotes recomendado para rapidez e isolamento de ambientes.
* Docker & Docker Compose: Necessários para subir a base de dados PostgreSQL e correr a aplicação em contentores.
* Google Cloud API Key: Chave com as APIs Places e Geocoding ativadas.

2. Variáveis de Ambiente
* Cria um arquivo chamado .env na raiz do projeto e adiciona a tua chave:

```
GOOGLE_API_KEY=tua_chave_aqui
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/recommendations
```

3. Instalação Local
* Se optares por rodar o projeto fora do Docker, utiliza o uv através do comando:

```
make install-local
```

## 🏃 Como Executar

1. Localmente

* Para iniciar o servidor em modo de desenvolvimento (com auto-reload):

```
make run-local
```
* Nota: Este modo requer que a base de dados PostgreSQL esteja ativa (pode usar o comando docker compose up -d db para subir apenas o banco).

2. Via Docker (Recomendado)

* Este comando sobe a API e a Base de Dados PostgreSQL automaticamente em contentores isolados:

```
make run
```
* API disponível em: http://localhost:8000
* Logs: O comando já inicia o acompanhamento dos logs do contentor.

# 🧪 Testes
Para garantir que tudo está funcionando corretamente:

```
# Testar dentro do contentor Docker
make test

# Testar no ambiente local
make test-local
```

## 📖 Documentação da API
Após iniciar o servidor, acesse a documentação interativa gerada pelo FastAPI:

* Swagger UI: http://127.0.0.1:8000/docs
