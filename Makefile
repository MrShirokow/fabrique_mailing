# for developing
local:
	python manage.py runserver

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
