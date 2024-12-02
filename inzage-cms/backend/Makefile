dev:
	poetry run uvicorn app.main:app --reload --port 8000	
migration_head:
	poetry run alembic -c alembic/alembic.ini upgrade head
test:
	poetry run coverage run -m pytest && poetry run coverage report -m
type_fix:
	poetry run ruff format app
	poetry run ruff format alembic
	poetry run ruff format tests
	poetry run ruff check app --fix
	poetry run ruff check alembic --fix
	poetry run ruff check tests --fix
db:
	docker compose --env-file .env up -d dbgate