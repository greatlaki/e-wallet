lint:
	cd backend && ./manage.py makemigrations --check --no-input --dry-run
	flake8 backend
	cd backend && mypy

test:
	cd backend && pytest --ff -x --cov-report=xml --cov=. --cov-append -m 'single_thread'
	cd backend && pytest --dead-fixtures