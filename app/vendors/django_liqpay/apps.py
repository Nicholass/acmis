from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DjangoLiqpayConfig(AppConfig):
    name = 'vendors.django_liqpay'
    verbose_name = _('Liqpay')
