# Mailing
**Mailing** is a WEB application for creating and sending notifications

## `Docker` installation
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## `docker-compose` installation
https://docs.docker.com/compose/install/

## Run project
### with make
```bash
make run
```

### without make
```bash
docker-compose build
docker-compose up
docker exec notification_app python manage.py migrate
```
## Create `superuser` for django admin
### with make
```bash
make superuser
```
### without make
```bash
docker exec -it notification_app python manage.py createsuperuser
```

## .env file example:
```
DEBUG=True
PORT=8000

POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=my_login
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_SECRET=my_api_key

OPEN_API_TOKEN=my_jwt_token
MAILING_SERVICE_URL=https://probe.fbrq.cloud/v1/send/1
CONTENT_TYPE=application/json
ACCEPT=application/json
```

## Start tests
### install requirements
```bash
pip install -r requirements.txt 
```
### run with make
```bash
make test
```
### run without make
```bash
pytest -v -p no:warnings
```
