#!/bin/bash

mkdir /etc/opendkim/keys
mkdir /etc/opendkim/keys/diggers.kiev.ua
cd /etc/opendkim/keys/diggers.kiev.ua
if [ ! -f "mail.txt" ]
then
    opendkim-genkey -s mail -d diggers.kiev.ua
fi

cd /tmp
/usr/bin/supervisord -c /etc/supervisord.conf
/opt/postfix.sh
