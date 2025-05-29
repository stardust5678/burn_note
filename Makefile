test:
	coverage run --rcfile=.coveragerc manage.py test

start-web:
	npm run dev

start-api:
	$(MAKE) start-db
	cd burn_note_api && fastapi dev api/main.py

start-db:
	docker ps -a --format '{{.Names}}' | grep -q '^burn-note-db$$' || \
	docker run --name burn-note-db -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=burn_note -p 5432:5432 -d postgres