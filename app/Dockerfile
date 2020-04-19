FROM python:3.6

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update -qq
RUN apt-get install -y gettext libsasl2-dev python-dev libldap2-dev libssl-dev

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 8000
