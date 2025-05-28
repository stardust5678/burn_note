migrate:
	python manage.py makemigrations
	python manage.py migrate

requirements:
	pip install -qr requirements.txt --exists-action w

start:
	python manage.py runserver

test:
	coverage run --rcfile=.coveragerc manage.py test

start-api:
	$(MAKE) start-db
	fastapi dev api/main.py

start-db:
	docker ps -a --format '{{.Names}}' | grep -q '^burn-note-db$$' || \
	docker run --name burn-note-db -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=burn_note -p 5432:5432 -d postgres