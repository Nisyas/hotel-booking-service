.PHONY: install run test lint format docker-up docker-down migrate shell

install:
	poetry install

run:
	poetry run python manage.py runserver 0.0.0.0:9000

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=. --cov-report=html

lint:
	poetry run ruff check .

format:
	poetry run ruff check --fix .
	poetry run ruff format .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose up --build -d

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

shell:
	poetry run python manage.py shell

createsuperuser:
	poetry run python manage.py createsuperuser

logs:
	docker-compose logs -f app

db-shell:
	docker-compose exec db psql -U postgres -d hotel_booking_db

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage
