server:
	cd backend && ./manage.py migrate && ./manage.py runserver

test:
	cd backend && pytest --ff -x --cov-report=xml --cov=. --cov-append -m 'single_thread'
	cd backend && pytest --dead-fixtures
