FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y postfix supervisor syslog-ng-core opendkim opendkim-tools && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 25

RUN	sed -i -E 's/^(\s*)system\(\);/\1unix-stream("\/dev\/log");/' /etc/syslog-ng/syslog-ng.conf # Uncomment 'SYSLOGNG_OPTS="--no-caps"' to avoid the following warning: # syslog-ng: Error setting capabilities, capability management disabled; error='Operation not permitted' # http://serverfault.com/questions/524518/error-setting-capabilities-capability-management-disabled# RUN	sed -i 's/^#\(SYSLOGNG_OPTS="--no-caps"\)/\1/g' /etc/default/syslog-ng

COPY ./postfix.sh /opt/postfix.sh
COPY ./virtual /etc/postfix/virtual
COPY ./supervisord.conf /etc/supervisord.conf
COPY ./opendkim.conf /etc/opendkim.conf

RUN echo 'SOCKET="inet:12301@localhost"' >> /etc/default/opendkim

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
