.ONESHELL:

init:
	echo COMPOSE_PROJECT_NAME=chrome-headless-service > .env
	echo PROJECT_VERSION=local >> .env

build:
	docker-compose -f docker-compose.yml build

build-live:
	docker-compose -f docker-compose-live.yml build
