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

# Доп. задания:
3 - Реализована контейнеризация в Docker  
6 - Админка Django вроде подходит под описание  
12 - Сделано логирование запросов на API и при работе с внешним API. 
Формат не совсем тот, что описан, 