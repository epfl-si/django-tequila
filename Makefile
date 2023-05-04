.PHONY: build init-db up stop logs reset hard-reset test test1 test2 \
	bash shell pep8

ifeq ($(DOCKERFILES),)
#DOCKERFILES := -f sample_app/python3-6-django-1/docker-compose.yml
#DOCKERFILES := -f sample_app/python3-8-django-2/docker-compose.yml
DOCKERFILES := -f sample_app/python3-8-django-4/docker-compose.yml
endif

superadmin:
	docker compose $(DOCKERFILES) exec -T web python manage.py shell < sample_app/create_superadmin.py

build:
	docker compose $(DOCKERFILES) build

init-db: up
	docker compose $(DOCKERFILES) exec web python manage.py makemigrations
	docker compose $(DOCKERFILES) exec web python manage.py makemigrations django_tequila_app
	docker compose $(DOCKERFILES) exec web python manage.py migrate
	make superadmin

up:
	docker compose $(DOCKERFILES) up --detach

down:
	docker compose $(DOCKERFILES) down

stop:
	docker compose $(DOCKERFILES) stop

logs:
	docker compose $(DOCKERFILES) logs -f

reset: build up init-db

hard-reset:
	docker compose $(DOCKERFILES) down --rmi all -v

test:
	docker compose $(DOCKERFILES) -f docker compose.test.yml build
	docker compose $(DOCKERFILES) -f docker compose.test.yml up -d
	docker compose $(DOCKERFILES) -f docker compose.test.yml exec web pytest

bash: up
	docker compose $(DOCKERFILES) exec web bash

shell: up
	docker compose $(DOCKERFILES) exec web python manage.py shell_plus

pep8:
	flake8 . --max-line-length=120 --exclude=migrations

