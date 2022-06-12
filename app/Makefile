init:
	poetry install

run:
	poetry run uvicorn src.main:app --reload

test:
	poetry run pytest

migration-revision:
	poetry run alembic revision --autogenerate

migration-upgrade:
	poetry run alembic upgrade head
