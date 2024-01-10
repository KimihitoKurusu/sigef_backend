# Makefile

.PHONY: install run migrate superuser

setup:
	sudo docker network create sigef_local_network || true
	sudo docker-compose -f docker-compose.local.yml build
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py createsuperuser

build:
	sudo docker-compose -f docker-compose.local.yml build

install:
	pipenv install

down:
	sudo docker-compose -f docker-compose.local.yml down
start:
	sudo docker-compose -f docker-compose.local.yml up web

make-migrations:
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations

merge-migrations:
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations --merge

migrate:
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate

superuser:
	pipenv run python manage.py createsuperuser
clear-volumes:
	sudo docker-compose -f docker-compose.local.yml down -v

dbshell:
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py dbshell

managepy:
	sudo docker-compose -f docker-compose.local.yml run --rm web python manage.py $(ARGS)

pgadmin:
	sudo docker-compose -f docker-compose.local.yml up pgadmin