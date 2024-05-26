FROM python:3.12-slim-bullseye

LABEL authors="jay"

ARG ENV_FILE
COPY ${ENV_FILE} /usr/src/tg/.env

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/tg

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/tg/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/tg/

ENTRYPOINT ["python", "bot.py"]
