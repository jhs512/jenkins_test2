FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
COPY . .

RUN pip3 install -r requirements.txt \
    && apt-get update