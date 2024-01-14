up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

server:
	cd backend && ./manage.py migrate && ./manage.py runserver

lint:
	poetry run ruff .

test:
	poetry run coverage run -m pytest
