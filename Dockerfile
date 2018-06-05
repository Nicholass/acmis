FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY bower.json ./

RUN apt-get update -qq
RUN apt-get install -y -qq git curl wget gettext

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -y nodejs

RUN npm install --global bower

RUN pip install virtualenv
RUN virtualenv --python=python3 --prompt="ACIS" acis_venv
RUN . ./acis_venv/bin/activate

RUN pip install -r ./requirements.txt
RUN pip install https://bitbucket.org/slav0nic/djangobb/get/stable.tar.gz
RUN pip install git+https://github.com/arneb/django-messages.git@master

COPY . .

EXPOSE 8000