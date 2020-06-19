# Project configuration.
PROJECT_NAME = pyconsql

# Makefile variables.
SHELL = /bin/bash

# Makefile parameters.
RUN ?= local
TAG ?= $(shell git describe)

# Misc.
TOPDIR = $(shell git rev-parse --show-toplevel)

.PHONY: local-api
local-api: ## Run connexion locally
	export CONNEXION_SETTINGS_MODULE=$(PROJECT_NAME).api.settings.local \
	&& poetry run gunicorn \
		--reload \
		--timeout 1800 \
		--log-level debug \
		-b 0.0.0.0:8000 \
		--worker-class aiohttp.GunicornUVLoopWebWorker \
		$(PROJECT_NAME).wsgi

.PHONY: make_migrations
make_migrations: ## Make new migrations
	NEXT_ID=$(shell ls alembic/versions/ | grep -c *.py)
	poetry run alembic revision --autogenerate -m "$(M)" --rev-id=`printf "%04d" ${NEXT_ID}`

.PHONY: migrate
migrate: ## Apply migrations
	poetry run alembic upgrade head
