.PHONY: env
env:
	cp .env.example .env

.PHONY: build
build:
	docker compose -f compose.dev.yml build

build--no-cache:
	docker compose -f compose.dev.yml build --no-cache

.PHONY: up
up:
	docker compose -f compose.dev.yml up

.PHONY: up-d
up-d:
	docker compose -f compose.dev.yml up -d

.PHONY: dev
dev:
	@make build
	@make up-d

.PHONY: exec
exec:
	docker compose -f compose.dev.yml exec api bash

.PHONY: exec-db
exec-db:
	docker compose -f compose.dev.yml exec db bash

.PHONY: logs
logs:
	docker compose -f compose.dev.yml logs -f

.PHONY: stop
stop:
	docker compose -f compose.dev.yml stop

.PHONY: kill
kill:
	docker compose -f compose.dev.yml kill

.PHONY: down
down:
	docker compose -f compose.dev.yml down

.PHONY: prune
prune:
	docker image prune

.PHONY: clean
clean:
	docker rm -f `docker ps -aq`
	docker system prune -af

.PHONY: remove-none
remove-none:
	docker images | awk '/none/{print $3}' | xargs docker rmi

.PHONY: test
test:
	docker compose -f compose.dev.yml exec api python manage.py test --parallel --settings=config.tests

.PHONY: black
black:
	docker compose -f compose.dev.yml exec api black .

.PHONY: isort
isort:
	docker compose -f compose.dev.yml exec api isort .

.PHONY: flake8
flake8:
	docker compose -f compose.dev.yml exec api flake8 .

.PHONY: lint
lint:
	@make black
	@make isort
	@make flake8

