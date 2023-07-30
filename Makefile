server:
	cd backend && ./manage.py migrate && ./manage.py runserver

lint:
	poetry run ruff .

test:
	poetry run coverage run -m pytest
	poetry run coverage report
