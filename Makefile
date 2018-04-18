.PHONY: build up stop logs reset test test1 test2 \
	bash shell

ifeq ($(DOCKERFILES),)
DOCKERFILES := -f docker-compose-django2.yml -f docker-compose.test.yml
endif

build:
	docker-compose $(DOCKERFILES) build

up:
	docker-compose $(DOCKERFILES) up -d

down:
	docker-compose $(DOCKERFILES) down

stop:
	docker-compose $(DOCKERFILES) stop

logs:
	docker-compose $(DOCKERFILES) logs -f

reset: build up

test:
	docker-compose $(DOCKERFILES) exec web pytest

bash: up
	docker-compose $(DOCKERFILES) exec web bash

shell: up
	docker-compose $(DOCKERFILES) exec web python manage.py shell
