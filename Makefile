server:
	cd backend && ./manage.py migrate && ./manage.py runserver

test:
	poetry run coverage run -m pytest
	poetry run coverage report
