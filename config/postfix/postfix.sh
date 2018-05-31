#!/bin/bash

# fix postfix settings virtual
echo "virtual_alias_domains = "$DOMAINS >> /etc/postfix/main.cf
echo "virtual_alias_maps = hash:/etc/postfix/virtual" >> /etc/postfix/main.cf

#add opendkim support
echo "milter_protocol = 2" >> /etc/postfix/main.cf
echo "milter_default_action = accept" >> /etc/postfix/main.cf
echo "smtpd_milters = inet:localhost:12301" >> /etc/postfix/main.cf
echo "non_smtpd_milters = inet:localhost:12301" >> /etc/postfix/main.cf

# add docker network
sed -i 's/^mynetworks.*/mynetworks = 172.0.0.0\/8/' /etc/postfix/main.cf

#sed -i 's/smtpd_use_tls = yes/smtpd_use_tls = no/' /etc/postfix/main.cf

postmap /etc/postfix/virtual
service postfix reload
service postfix restart
service opendkim restart
tail -f /var/log/mail.log