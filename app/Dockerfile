FROM python:3.6

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update -qq
RUN apt-get install -y gettext

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 8000
