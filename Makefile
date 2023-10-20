# project variables
COMPOSE_FILE ?= -f docker-compose.yml
PROJ_NAME ?= fast-app

# Aesthetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "WARNING: $$1"; printf $(NC)' MESSAGE

.PHONY: dev stop install

install:
	${INFO} "Installing requirements for backend service"
	@pip3 install -r requirements.txt

stop:
	${INFO} "Resetting fast API containers..."
    ifeq ($(shell docker ps -a --format '{{.Names}}' | grep $(PROJ_NAME)), $(PROJ_NAME))
		docker stop $(PROJ_NAME)
		docker rm $(PROJ_NAME)
    endif

dev: stop
	${INFO} "Spinning up backend fast API locally..."
	@docker-compose $(COMPOSE_FILE) build
	@docker-compose $(COMPOSE_FILE) up --force-recreate
