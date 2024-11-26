DCE=docker-compose exec

build: 
	docker-compose up -d --build
	
start:
	@docker-compose up -d

down:
	@docker-compose down

bash:
	@${DCE} django bash

secret-key:
	@${DCE} django python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' openssl rand -base64 32

migrate:
	@${DCE} django python manage.py makemigrations && \
	${DCE} django python manage.py migrate
