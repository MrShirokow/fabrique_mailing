run:
	python manage.py runserver

makemig:
	python manage.py makemigrations

migrate:
	python manage.py migrate

su:
	python manage.py createsuperuser