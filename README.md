# 📍 API de Recomendação de Lugares

Esta é uma API moderna desenvolvida com **FastAPI** que permite procurar recomendações de lugares (restaurantes, museus, parques, etc.) utilizando a **Google Places API**. O projeto foi estruturado seguindo boas práticas de programação, incluindo injeção de dependência para testes e contentorização com Docker.

## 🚀 Funcionalidades

* **Busca de Lugares:** Consulta a API do Google para obter nomes, moradas, classificações e tipos de locais.
* **Health Check:** Endpoint para verificar se a API está online.
* **Arquitetura Limpa:** Separação clara entre rotas, esquemas de dados (Pydantic) e serviços externos.
* **Testes Automatizados:** Suite de testes com mocks para simular a API do Google sem gastar créditos.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI:** Framework web de alta performance.
* **Uvicorn:** Servidor ASGI para correr a aplicação.
* **HTTPX:** Cliente HTTP assíncrono para comunicar com o Google.
* **UV:** Gestor de pacotes e ambientes Python extremamente rápido.
* **Docker:** Para facilitar a implementação em qualquer ambiente.

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── config.py      # Gestão de variáveis de ambiente
│   ├── main.py        # Pontos de entrada (endpoints) da API
│   ├── schemas.py     # Modelos de dados (Pydantic)
│   ├── services.py    # Lógica de integração com a API do Google
│   └── __init__.py
├── tests/
│   └── test_main.py   # Testes unitários e de integração
├── Dockerfile         # Configuração da imagem Docker
├── Makefile           # Atalhos para comandos comuns
├── pyproject.toml     # Dependências do projeto
└── .env               # Variáveis sensíveis (não incluído no Git)
```

## ⚙️ Configuração Inicial

1. Pré-requisitos
* Ter o Python 3.12+ instalado.
* Ter o uv instalado (recomendado).
* Uma chave de API da Google Cloud (com a Places API ativada).

2. Variáveis de Ambiente
* Cria um ficheiro chamado .env na raiz do projeto e adiciona a tua chave:

```
GOOGLE_API_KEY=a_tua_chave_aqui_sem_aspas
```

3. Instalação
* Se usares o uv (conforme definido no teu Makefile):

```
make install
```

## 🏃 Como Executar
1. Localmente

* Para iniciar o servidor em modo de desenvolvimento (com auto-reload):

```
make run
```

A API ficará disponível em: http://127.0.0.1:8000

2. Via Docker

* Se preferires usar contentores:

```
docker build -t api-recomendacao .
docker run -p 8000:8000 --env-file .env api-recomendacao
```

# 🧪 Testes
Para garantir que tudo está a funcionar 
corretamente:

```
make test
```

## 📖 Documentação da API
Após iniciar o servidor, podes aceder à documentação interativa:

* Swagger UI: http://127.0.0.1:8000/docs

* Redoc: http://127.0.0.1:8000/redoc
