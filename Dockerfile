FROM ubuntu:latest

MAINTAINER Romulus Darwin

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt -y install tzdata

# Python3.11 installation
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.11 python3-pip -y
#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN apt install curl -y

# Setup for poetry (python project dependency manager)
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_NO_INTERACTION=1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/opt/poetry/bin"

# wsgi installation (gunicorn)
RUN apt install gunicorn -y

# Copy src files
COPY . /blitz_api
WORKDIR /blitz_api

# Install project dependencies
RUN poetry config installer.max-workers 10
RUN poetry install

