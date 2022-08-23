# pull official base image
FROM python:3.10-slim-bullseye

# set work directory
WORKDIR /usr/src/app/

# copy requirements.txt
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .
