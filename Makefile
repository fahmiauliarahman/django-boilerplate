.PHONY: help install sync sync-all run migrate makemigrations shell superuser test check deploy-check collectstatic clean

PYTHON ?= uv run python
MANAGE ?= $(PYTHON) manage.py
ENV_PORT := $(shell [ -f .env ] && grep '^APP_PORT=' .env | cut -d'=' -f2 | tr -d '"[:space:]')

# 2. Use terminal environment PORT, otherwise the .env PORT, otherwise fallback to 8000
ifneq ($(ENV_PORT),)
    PORT ?= $(ENV_PORT)
else
    PORT ?= 8000
endif

help:
	@printf '%s\n' \
		'Common targets:' \
		'  make install            Install dependencies' \
		'  make run                Run development server' \
		'  make migrate            Apply migrations' \
		'  make makemigrations     Create migrations' \
		'  make shell              Open Django shell' \
		'  make superuser          Create admin user' \
		'  make test               Run tests' \
		'  make check              Run system checks' \
		'  make deploy-check       Run deployment checks' \
		'  make collectstatic      Collect static files' \
		'  make clean              Remove Python caches' \
		'  make create-app NAME=x  Remove Python caches'

install sync:
	uv sync

sync-all:
	uv sync --all-groups

run:
	$(MANAGE) runserver $(PORT)

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

shell:
	$(MANAGE) shell

superuser:
	$(MANAGE) createsuperuser

test:
	$(MANAGE) test

check:
	$(MANAGE) check

deploy-check:
	$(MANAGE) check --deploy

collectstatic:
	$(MANAGE) collectstatic --noinput

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

create-app:
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Error: You must specify a module name. Usage: make create-app NAME=my_module"; \
		exit 1; \
	fi
	$(MANAGE) startapp $(NAME)
	@echo "✅ Django module '$(NAME)' created successfully!"
