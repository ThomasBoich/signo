FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive 
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app
RUN apt -y update && apt -y upgrade

RUN apt -y install nano

RUN apt -y install locales locales-all && locase-gen en_US.UTF-8 ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LANGUAGE=ru_RU:ru

ADD requirements.txt /app/src/

RUN python3 -m pip install -r /app/src/requirements.txt -U

ADD . /app/src/

RUN python3 -m pip install -r /app/src/reuqirements.txt -U

WORKDIR /app/src

EXPOSE 80