dev:
	poetry install --with dev
	alembic upgrade head
	poetry run uvicorn app.main:app --reload