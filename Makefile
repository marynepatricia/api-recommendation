PYTHON := uv run python

.PHONY: help install run stop test clean-db install-local run-local test-local

help: 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


build: 
	docker compose build

run: 
	docker compose up -d --build
	@echo "API disponível em: http://localhost:8000"
	docker compose logs -f api

stop: 
	docker compose down

test:
	docker compose run --rm api pytest

clean-db:
	docker compose run --rm db psql -h db -U user -d recommendations -c "TRUNCATE TABLE search_history;"



install-local:
	uv sync

run-local:
	uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test-local:
	uv run pytest

lint:
	uv run pylint app/