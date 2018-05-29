FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY bower.json ./

RUN apt-get update -qq
RUN apt-get install -y -qq git curl wget

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -y nodejs

RUN npm install --global bower

RUN pip install virtualenv
RUN virtualenv --python=python3 --prompt="ACIS" acis_venv
RUN . ./acis_venv/bin/activate

RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 8000

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y postfix supervisor syslog-ng-core && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 25

RUN	sed -i -E 's/^(\s*)system\(\);/\1unix-stream("\/dev\/log");/' /etc/syslog-ng/syslog-ng.conf # Uncomment 'SYSLOGNG_OPTS="--no-caps"' to avoid the following warning: # syslog-ng: Error setting capabilities, capability management disabled; error='Operation not permitted' # http://serverfault.com/questions/524518/error-setting-capabilities-capability-management-disabled# RUN	sed -i 's/^#\(SYSLOGNG_OPTS="--no-caps"\)/\1/g' /etc/default/syslog-ng

ADD ./config/postfix/postfix.sh /opt/postfix.sh
ADD ./config/postfix/virtual /etc/postfix/virtual
ADD ./config/postfix/supervisord.conf /supervisord.conf