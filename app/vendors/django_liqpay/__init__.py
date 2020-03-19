VERSION = (0, 0, 1,)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'vendors.django_liqpay.apps.DjangoLiqpayConfig'

import base64
import hashlib
import json
from urllib.parse import urljoin

from .forms import ApiForm, CheckoutForm
from .exceptions import LiqPayValidationError
from .settings import \
    LIQPAY_DEFAULT_CURRENCY, \
    LIQPAY_DEFAULT_LANGUAGE,\
    LIQPAY_DEFAULT_ACTION,\
    LIQPAY_PUBLIC_KEY,\
    LIQPAY_PRIVATE_KEY


class LiqPay(object):

    host = 'https://www.liqpay.ua/api/'

    checkout_url = urljoin(host, '3/checkout/')

    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    def get_checkout_form(self, **kwargs):

        params = self._clean_api_params(**kwargs)

        data = base64.b64encode(json.dumps(params).encode())

        return CheckoutForm(self.checkout_url, data={
            'data': data,
            'signature': self._make_signature(data)
        })    

    def _clean_api_params(self, **kwargs):

        params = {
            'version': 3,
            'currency': settings.LIQPAY_DEFAULT_CURRENCY,
            'language': settings.LIQPAY_DEFAULT_LANGUAGE,
            'action': settings.LIQPAY_DEFAULT_ACTION,
            'public_key': self._public_key
        }

        params.update(kwargs)

        form = ApiForm(data=params)

        if not form.is_valid():
            raise LiqPayValidationError(
                'Invalid params: %s' % ', '.join(form.errors.keys()))

        return form.cleaned_data

    def _make_signature(self, data):
        params = [self._private_key, data.decode(), self._private_key]
        fields = ''.join(params)
        return base64.b64encode(hashlib.sha1(fields.encode()).digest())

liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
