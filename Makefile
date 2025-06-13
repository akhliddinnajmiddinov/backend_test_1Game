dev:
	docker compose up -d --build
	@echo "Application running at http://localhost:8000/docs"

migrate:
	docker compose run --rm app poetry run alembic revision --autogenerate -m "Auto migration"
	docker compose run --rm app poetry run alembic upgrade head

test:
	docker compose run --rm app poetry run pytest

down:
	docker compose down -v

logs:
	docker compose logs -f