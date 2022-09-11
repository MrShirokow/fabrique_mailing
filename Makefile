all: makemig migrate up

run: build up

makemig:
	python manage.py makemigrations

migrate:
	docker exec notification_app python manage.py migrate

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

imageprune:
	docker image prune -f

superuser:
	docker exec -it notification_app python manage.py createsuperuser

cronadd:
	docker exec -it notification_app python manage.py crontab add

cronshow:
	docker exec -it notification_app python manage.py crontab show

cronremove:
	docker exec -it notification_app python manage.py crontab remove

bash:
	docker exec -it notification_app /bin/bash

test:
	pytest -v -p no:warnings
