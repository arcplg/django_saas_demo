DCE=docker-compose exec

.PHONY: build
build: 
	docker-compose up -d --build

setup: migrate
	@${DCE} django python manage.py assets_pull
	@${DCE} django python manage.py collectstatic --noinput

.PHONY: start
start:
	@docker-compose up -d

.PHONY: down
down:
	@docker-compose down

.PHONY: bash
bash:
	@${DCE} django bash

.PHONY: secret-key
secret-key:
	@${DCE} django python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' openssl rand -base64 32

.PHONY: migrate
migrate:
	@${DCE} django python manage.py makemigrations && \
	${DCE} django python manage.py migrate

.PHONY: startapp
startapp:
	@if [ -z "$(app_name)" ]; then \
		echo "Error: app_name is required"; \
		exit 1; \
	fi
	@${DCE} django bash -c "mkdir -p /usr/src/code/apps/$(app_name) && cd /usr/src/code && python manage.py startapp $(app_name) apps/$(app_name) || true"
