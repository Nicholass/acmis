#!/bin/bash

# fix postfix settings virtual
echo "virtual_alias_domains = mail.diggers.kiev.ua localhost" >> /etc/postfix/main.cf
echo "virtual_alias_maps = hash:/etc/postfix/virtual" >> /etc/postfix/main.cf

#add opendkim support
echo "milter_protocol = 2" >> /etc/postfix/main.cf
echo "milter_default_action = accept" >> /etc/postfix/main.cf
echo "smtpd_milters = inet:localhost:12301" >> /etc/postfix/main.cf
echo "non_smtpd_milters = inet:localhost:12301" >> /etc/postfix/main.cf

# add docker network
sed -i 's/^myhostname.*/myhostname = diggers.kiev.ua/' /etc/postfix/main.cf
sed -i 's/^mydestination.*/mydestination = $myhostname, localhost, $mydomain/' /etc/postfix/main.cf
echo "mydomain = diggers.kiev.ua" >> /etc/postfix/main.cf

echo "myorigin = " >> /etc/postfix/main.cf
echo "relay_domains = " >> /etc/postfix/main.cf
sed -i 's/^myorigin.*/myorigin = $mydomain/' /etc/postfix/main.cf
sed -i 's/^relay_domains.*/relay_domains = $mydestination/' /etc/postfix/main.cf

sed -i 's/^mynetworks.*/mynetworks = 172.0.0.0\/8/' /etc/postfix/main.cf

#sed -i 's/smtpd_use_tls = yes/smtpd_use_tls = no/' /etc/postfix/main.cf

postmap /etc/postfix/virtual
service postfix restart
service opendkim restart
tail -f /var/log/mail.log
