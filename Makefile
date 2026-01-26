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

# Comando para apagar dados do banco de dados
clean-db:
	docker compose exec db psql -U user -d recommendations -c "TRUNCATE TABLE search_history;"