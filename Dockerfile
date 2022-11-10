FROM python:3.10-slim-bullseye

WORKDIR /usr/src/app/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
