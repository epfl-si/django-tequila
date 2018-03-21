.PHONY: build up stop logs reset test bash

build:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down

stop:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml stop

logs:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml logs -f

reset: build up
	@echo 'resetting'

test: up
	docker-compose -f docker-compose.yml -f docker-compose.test.yml exec web pytest

bash: up
	docker-compose -f docker-compose.yml -f docker-compose.test.yml exec web bash
