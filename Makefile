dev:
	docker compose up -d --build
	@echo "Application running at http://localhost:8000/docs"

migrate:
	docker compose run --rm app poetry run alembic revision --autogenerate -m "Auto migration"
	docker compose run --rm app poetry run alembic upgrade head
	docker compose down -v
	
test:
	ls
	docker compose run --rm app poetry run pytest tests/test_tournament.py
	docker compose down -v
	
down:
	docker compose down -v

logs:
	docker compose logs -f
