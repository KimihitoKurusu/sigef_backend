# Makefile

.PHONY: install run migrate superuser

install:
	pipenv install

start:
	pipenv run python manage.py runserver

migrate:
	pipenv run python manage.py migrate

makemigrations:
	pipenv run python manage.py makemigrations

superuser:
	pipenv run python manage.py createsuperuser
