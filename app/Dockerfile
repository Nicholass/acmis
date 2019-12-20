FROM python:3.6

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update -qq
RUN apt-get install -y gettext

COPY . .

RUN pip install -r ./requirements.txt
RUN pip install ./packages/django-messages-master.zip

EXPOSE 8000
