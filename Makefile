THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up shell destroy down
build:
	docker-compose -f docker-compose.yml build $(c)
up:
	docker-compose -f docker-compose.yml up -d $(c)
bash:
	docker-compose -f docker-compose.yml exec backend /bin/bash $(c)
destroy:
	docker-compose -f docker-compose.yml down -v $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
