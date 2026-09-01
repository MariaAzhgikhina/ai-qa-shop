PYTEST ?= .venv/bin/pytest

.PHONY: up down api e2e

up:
	docker compose up --build -d
	@printf "\nAI QA Shop is starting:\n  Catalog: http://localhost:8000/\n  Swagger: http://localhost:8000/docs\n\n"

down:
	docker compose down

api:
	$(PYTEST) -vv tests/api

e2e:
	$(PYTEST) -vv tests/e2e
