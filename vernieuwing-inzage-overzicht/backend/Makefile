dev:
	poetry run uvicorn app.main:app --reload --port 8001
test:
	poetry run coverage run -m pytest && poetry run coverage report
type_fix:
	poetry run ruff format app
	poetry run ruff format common
	poetry run ruff format tests
	poetry run ruff check app --fix
	poetry run ruff check common --fix
	poetry run ruff check tests --fix