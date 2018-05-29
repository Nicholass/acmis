#!/bin/bash

# fix postfix settings virtual
echo "virtual_alias_domains = "$DOMAINS >> /etc/postfix/main.cf
echo "virtual_alias_maps = hash:/etc/postfix/virtual" >> /etc/postfix/main.cf

# add docker network
sed -i 's/^mynetworks.*/mynetworks = 172.0.0.0\/8/' /etc/postfix/main.cf

#sed -i 's/smtpd_use_tls = yes/smtpd_use_tls = no/' /etc/postfix/main.cf

postmap /etc/postfix/virtual
service postfix reload
service postfix restart
tail -f /var/log/mail.log