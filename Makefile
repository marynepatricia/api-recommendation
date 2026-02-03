.PHONY: run stop build test clean-db install

# Instala dependências locais
install:
	uv sync

# Sobe o ambiente Docker e mostra logs
run:
	docker compose up -d --build
	docker compose logs -f api

# Para os serviços
stop:
	docker compose down

# Executa testes dentro do Docker
test:
	docker compose run --rm api pytest

# Limpa a tabela de cache
clean-db:
	docker compose run --rm db psql -h db -U user -d recommendations -c "TRUNCATE TABLE search_history;"