FROM python:3.10

RUN apt-get -y update && apt-get install -y cron

WORKDIR /usr/src/app/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
