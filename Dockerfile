FROM python:3.8.7

ENV MICRO_SERVICE=/usr/src/app

WORKDIR $MICRO_SERVICE

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt update

COPY ./app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . $MICRO_SERVICE