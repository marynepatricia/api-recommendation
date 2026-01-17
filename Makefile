.PHONY: run install test clean

# Comando para instalar as dependências usando o uv
install:
	uv sync

# Comando para rodar a API
run:
	uv run uvicorn app.main:app --reload

# Comando para rodar os testes
test:
	uv run pytest