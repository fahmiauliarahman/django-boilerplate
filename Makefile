.PHONY: help install sync sync-all run migrate makemigrations shell superuser test check deploy-check collectstatic clean

PYTHON ?= uv run python
MANAGE ?= $(PYTHON) manage.py
PORT ?= 8000

help:
	@printf '%s\n' \
		'Common targets:' \
		'  make install        Install dependencies' \
		'  make run            Run development server' \
		'  make migrate        Apply migrations' \
		'  make makemigrations Create migrations' \
		'  make shell          Open Django shell' \
		'  make superuser      Create admin user' \
		'  make test           Run tests' \
		'  make check          Run system checks' \
		'  make deploy-check   Run deployment checks' \
		'  make collectstatic  Collect static files' \
		'  make clean          Remove Python caches'

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
