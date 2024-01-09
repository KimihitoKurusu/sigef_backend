# Makefile

.PHONY: install run migrate superuser

setup:
	docker network create sigef_local_network || true
	docker-compose -f docker-compose.local.yml build
	docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate
	docker-compose -f docker-compose.local.yml run --rm web python manage.py createsuperuser

build:
	docker-compose -f docker-compose.local.yml build

install:
	pipenv install

down:
	docker-compose -f docker-compose.local.yml down
start:
	docker-compose -f docker-compose.local.yml up --attach web

make-migrations:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations

merge-migrations:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations --merge

migrate:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate

superuser:
	pipenv run python manage.py createsuperuser
clear-volumes:
	docker-compose -f docker-compose.local.yml down -v

dbshell:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py dbshell

managepy:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py $(ARGS)

pgadmin:
	docker-compose -f docker-compose.local.yml up --attach pgadmin