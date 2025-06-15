dev:
	docker compose up -d --build
	@echo "Application running at http://localhost:8000/docs"

migrate:
	docker compose run --rm app poetry run alembic revision --autogenerate -m "Auto migration"
	docker compose run --rm app poetry run alembic upgrade head
	
test:
	ls
	docker compose run --rm app poetry run pytest tests/test_tournament.py
	
lint:
	# Run code format check and linter
	docker compose run --rm app poetry run ruff check .
	# Run type checking
	docker compose run --rm app poetry run mypy .

down:
	docker compose down -v

logs:
	docker compose logs -f
