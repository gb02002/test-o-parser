FROM python:3.12-slim-bullseye

LABEL authors="jay"

ARG ENV_FILE
RUN set -o allexport; source ${ENV_FILE}; set +o allexport
RUN mkdir -p /usr/src/web

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev  \
    && rm -rf /var

# set work directory
WORKDIR /usr/src/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Delete build dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./entry.sh .
COPY ./run.sh
RUN sed -i 's/\r$//g' /usr/src/web/entry.sh
RUN chmod +x /usr/src/web/entry.sh

# copy project
COPY . .
RUN ls -la
RUN ./entry.sh
ENTRYPOINT ["/usr/src/web/run.sh"]
