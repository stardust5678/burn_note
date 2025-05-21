migrate:
	python manage.py makemigrations
	python manage.py migrate

requirements:
	pip install -qr requirements.txt --exists-action w

start:
	python manage.py runserver

test:
	coverage run --rcfile=.coveragerc manage.py test