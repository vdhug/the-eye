THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timescale login-api db-shell
up:
	docker-compose -f docker-compose.yml up -d $(c)
bash:
	docker-compose -f docker-compose.yml exec backend /bin/bash $(c)