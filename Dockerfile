# FROM python:3.8.7
FROM ubuntu:bionic

USER root

ENV MICRO_SERVICE=/usr/src/app

WORKDIR $MICRO_SERVICE

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt-get update

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb

RUN apt install -y python3.8
RUN apt install -y python3-pip

COPY ./app/requirements.txt .
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP
# RUN apt install -y firefox

# copy project
COPY . $MICRO_SERVICE