FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY bower.json ./

RUN apt-get update -qq
RUN apt-get install -y -qq git curl wget libjpeg62 zlib1g-dev imagemagick gettext

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -y nodejs

RUN npm install --global bower

RUN pip install -r ./requirements.txt

# Need a fix model migration file which have null field value without parameter Null=True. Maybe it fixed in new wersions
COPY ./packages/django-messages-master.zip ./
# We use a polymorphic model instead a model class for Posts. Package net to fix assertion is subclass of django model class check on tracking_analyzer/manager.py line 33-34
COPY ./packages/django-tracking-analyzer-master.zip ./
RUN pip install ./django-messages-master.zip && rm ./django-messages-master.zip && pip install ./django-tracking-analyzer-master.zip && rm ./django-tracking-analyzer-master.zip

COPY . .

EXPOSE 8000