"""
Error messages, data and custom validation code used in
django-registration's various user-registration form classes.

"""
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from confusable_homoglyphs import confusables

BAD_EMAIL_DOMAINS = [
    'aim.com',
    'aol.com',
    'email.com',
    'hotmail.com',
    'mailinator.com',
    'live.com',
    'yahoo.com'
]

# Below we construct a large but non-exhaustive list of names which
# users probably should not be able to register with, due to various
# risks:
#
# * For a site which creates email addresses from username, important
#   common addresses must be reserved.
#
# * For a site which creates subdomains from usernames, important
#   common hostnames/domain names must be reserved.
#
# * For a site which uses the username to generate a URL to the user's
#   profile, common well-known filenames must be reserved.
#
# etc., etc.
#
# Credit for basic idea and most of the list to Geoffrey Thomas's blog
# post about names to reserve:
# https://ldpreload.com/blog/names-to-reserve
SPECIAL_HOSTNAMES = [
    # Hostnames with special/reserved meaning.
    'autoconfig',     # Thunderbird autoconfig
    'autodiscover',   # MS Outlook/Exchange autoconfig
    'broadcasthost',  # Network broadcast hostname
    'isatap',         # IPv6 tunnel autodiscovery
    'localdomain',    # Loopback
    'localhost',      # Loopback
    'wpad',           # Proxy autodiscovery
]


PROTOCOL_HOSTNAMES = [
    # Common protocol hostnames.
    'ftp',
    'imap',
    'mail',
    'news',
    'pop',
    'pop3',
    'smtp',
    'usenet',
    'uucp',
    'webmail',
    'www',
]


CA_ADDRESSES = [
    'админ',
    'администратор',
    'модер',
    'модератор',
    'admin',
    'administrator',
    'moderator',
    'moder',
    'hostmaster',
    'info',
    'is',
    'it',
    'mis',
    'postmaster',
    'root',
    'ssladmin',
    'ssladministrator',
    'sslwebmaster',
    'sysadmin',
    'webmaster',
]


RFC_2142 = [
    # RFC-2142-defined names not already covered.
    'abuse',
    'marketing',
    'noc',
    'sales',
    'security',
    'support',
]


NOREPLY_ADDRESSES = [
    # Common no-reply email addresses.
    'mailer-daemon',
    'nobody',
    'noreply',
    'no-reply',
]


SENSITIVE_FILENAMES = [
    # Sensitive filenames.
    'clientaccesspolicy.xml',  # Silverlight cross-domain policy file.
    'crossdomain.xml',         # Flash cross-domain policy file.
    'favicon.ico',
    'humans.txt',
    'robots.txt',
    '.htaccess',
    '.htpasswd',
]


OTHER_SENSITIVE_NAMES = [
    # Other names which could be problems depending on URL/subdomain
    # structure.
    'account',
    'accounts',
    'blog',
    'buy',
    'clients',
    'contact',
    'contactus',
    'contact-us',
    'copyright',
    'dashboard',
    'doc',
    'docs',
    'download',
    'downloads',
    'enquiry',
    'faq',
    'help',
    'inquiry',
    'license',
    'login',
    'logout',
    'me',
    'myaccount',
    'payments',
    'plans',
    'portfolio',
    'preferences',
    'pricing',
    'privacy',
    'profile',
    'register'
    'secure',
    'settings',
    'signin',
    'signup',
    'ssl',
    'status',
    'subscribe',
    'terms',
    'tos',
    'user',
    'users'
    'weblog',
    'work',
]

DEFAULT_RESERVED_NAMES = (SPECIAL_HOSTNAMES + PROTOCOL_HOSTNAMES +
                          CA_ADDRESSES + RFC_2142 + NOREPLY_ADDRESSES +
                          SENSITIVE_FILENAMES + OTHER_SENSITIVE_NAMES)

def free_email(value):
  """
  Validator which disallows registration with
  email addresses from popular free webmail services moderately
  useful for preventing automated spam registrations.

  """

  if '@' not in value:
    return

  try:
    email_domain = value.split('@')[1]

    if email_domain.lower() in BAD_EMAIL_DOMAINS:
      raise ValidationError(_("Регистрация e-mail данного почтового сервиса запрещена."))
  except IndexError:
    pass

def reserved_name(value):
  """
  Validator which disallows many reserved names as form field
  values.

  """
  if not isinstance(value, six.text_type):
    return
  if value.lower() in DEFAULT_RESERVED_NAMES:
    raise ValidationError(_("Это имя пользователя зарезервировано."))

def validate_confusables(value):
    """
    Validator which disallows 'dangerous' usernames likely to
    represent homograph attacks.

    A username is 'dangerous' if it is mixed-script (as defined by
    Unicode 'Script' property) and contains one or more characters
    appearing in the Unicode Visually Confusable Characters file.

    """
    if not isinstance(value, six.text_type):
      return
    if confusables.is_dangerous(value):
      raise ValidationError(_("Это имя пользователя не может быть зарегистрировано."))


def validate_confusables_email(value):
    """
    Validator which disallows 'dangerous' email addresses likely to
    represent homograph attacks.

    An email address is 'dangerous' if either the local-part or the
    domain, considered on their own, are mixed-script and contain one
    or more characters appearing in the Unicode Visually Confusable
    Characters file.

    """
    if '@' not in value:
      return
    local_part, domain = value.split('@')
    if confusables.is_dangerous(local_part) or \
      confusables.is_dangerous(domain):
       raise ValidationError(_("Этот e-mail не может быть зарегистрирован."))
