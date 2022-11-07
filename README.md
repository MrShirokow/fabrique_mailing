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
make migrate
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
