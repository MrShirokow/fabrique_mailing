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

# Основное задание
Рассылка работает через планировщик `cron`. 
Текущая настройка сделана на запуск каждые 4 часа.
При успешной доставке на номер `number` этот номер больше не получит сообщения 
от текущей рассылки, если не будут обновлены атрибуты рассылки. 
В таком случае рассылка снова будет запущена для всех номеров,
которые удовлетворяют фильтру.

# Доп. задания:
3 - Реализована контейнеризация в Docker  
5 - По адресу /docs/ открывается Swagger UI со списком API методов  
6 - Админка Django вроде подходит под описание  
12 - Сделано логирование запросов на API и при отправке сообщений на внешнее API. 
Формат не совсем тот, что описан в задании, но при необходимости его можно изменить