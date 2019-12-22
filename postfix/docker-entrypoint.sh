#!/bin/bash

mkdir -p /etc/opendkim/keys
mkdir -p /etc/opendkim/keys/diggers.kiev.ua
cd /etc/opendkim/keys/diggers.kiev.ua
if [ ! -f "mail.txt" ]
then
    opendkim-genkey -s mail -d diggers.kiev.ua
    chown -R opendkim:opendkim mail.private
    chmod 600 mail.private
fi

/usr/bin/supervisord -c /etc/supervisord.conf
/opt/postfix.sh
