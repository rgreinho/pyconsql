# Project configuration.
PROJECT_NAME = pyconsql

# Makefile variables.
SHELL = /bin/bash

# Makefile parameters.
RUN ?= local
TAG ?= $(shell git describe)

# Misc.
TOPDIR = $(shell git rev-parse --show-toplevel)

.PHONY: help
help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

.PHONY: local-api
local-api: ## Run connexion locally
	export CONNEXION_SETTINGS_MODULE=$(PROJECT_NAME).api.settings.local \
	&& poetry run python pyconsql/main.py

.PHONY: migrations
migrations: ## Make new migrations
	NEXT_ID=$(shell ls alembic/versions/ | grep -c -e "\.py$$") \
	&& poetry run alembic revision --autogenerate --rev-id=`printf "%04d" $${NEXT_ID}` -m "$(M)"

.PHONY: migrate
migrate: ## Apply migrations
	poetry run alembic upgrade head

.PHONY: cleanup
cleanup: ## Delete the database and the migrations.
	rm -fr ./alembic/versions/*
	rm -fr petstore.db
