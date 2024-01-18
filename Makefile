# Makefile

.PHONY: install run migrate superuser

setup:
	 docker network create sigef_local_network || true
	 docker-compose -f docker-compose.local.yml build
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py createsuperuser

build:
	 docker-compose -f docker-compose.local.yml build

pipenv-install:
	pipenv install

down:
	 docker-compose -f docker-compose.local.yml down

start:
	 docker-compose -f docker-compose.local.yml up web

make-migrations:
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations

merge-migrations:
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations --merge

migrate:
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate

superuser:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py createsuperuser
	
clear-volumes:
	 docker-compose -f docker-compose.local.yml down -v

dbshell:
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py dbshell

managepy:
	 docker-compose -f docker-compose.local.yml run --rm web python manage.py $(ARGS)

pgadmin:
	 docker-compose -f docker-compose.local.yml up pgadmin

test:
	docker-compose -f docker-compose.test.yml -p sigef_backend_test run --rm web pytest $(arg)
	docker-compose -f docker-compose.test.yml -p sigef_backend_test down

test-build:
	docker-compose -f docker-compose.test.yml -p sigef_backend_test build

test-fast:
	docker-compose -f docker-compose.test.yml -p sigef_backend_test run --rm web pytest -vv --no-migrations $(arg)

test-lastfailed:
	docker-compose -f docker-compose.test.yml -p sigef_backend_test run --rm web pytest --no-migrations --lf $(arg)