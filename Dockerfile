FROM python:3.9

RUN apt-get -y update

WORKDIR /app

RUN pip install requests scrapy

copy ./app /app