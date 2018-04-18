include .env

.PHONY: build init-db up stop logs reset test test1 test2 \
	bash shell

ifeq ($(DOCKERFILES),)
DOCKERFILES := -f docker-compose-django2.yml -f docker-compose.test.yml
endif

superadmin:
	docker-compose $(DOCKERFILES) exec web \
	python manage.py shell -c "from django.contrib.auth import get_user_model; \
		User = get_user_model(); \
		User.objects.filter(email='${SUPER_ADMIN_EMAIL}').delete(); \
		User.objects.create_superuser('${SUPER_ADMIN_USERNAME}', '${SUPER_ADMIN_EMAIL}', '${SUPER_ADMIN_PASSWORD}');"

build:
	docker-compose $(DOCKERFILES) build

init-db: up
	docker-compose $(DOCKERFILES) exec web python manage.py makemigrations
	docker-compose $(DOCKERFILES) exec web python manage.py migrate
	make superadmin

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
