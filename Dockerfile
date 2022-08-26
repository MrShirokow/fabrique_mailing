# pull official base image
FROM python:3.10

# install cron
RUN apt-get update && apt-get install -y cron

# set work directory
WORKDIR /usr/src/app/

# copy requirements.txt
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip &&  \
    pip uninstall pytz && \
    pip uninstall tzdata && \
    pip install -r requirements.txt

# copy project
COPY . .
