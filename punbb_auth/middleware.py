from django.conf import settings
from .models import PunbbUser
from hashlib import md5
import random

PUNBB_COOKIE_NAME = settings.PUNBB_COOKIE_NAME
COOKIE_SEED = settings.COOKIE_SEED

# %d(size id) %d(id) %s(hash)
PUNCOOKIE_TPL = 'a%%3A2%%3A%%7Bi%%3A0%%3Bs%%3A%d%%3A%%22%d%%22%%3Bi%%3A1%%3Bs%%3A32%%3A%%22%s%%22%%3B%%7D'


class PunBBSessionMiddleware(object):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        # punbb cookie
        try:
            punbb_authentified = request.session.get('punbb_auth', None)
            if request.user.is_authenticated():
                if not punbb_authentified:
                    bbuser = PunbbUser.objects.get(username=request.user.username)
                    hash = md5.new(COOKIE_SEED + bbuser.password).hexdigest()
                    user_id = bbuser.id
                    idsize = len('%d' % user_id)
                    pun_cookie = PUNCOOKIE_TPL % (idsize, user_id, hash)
                    request.session['punbb_auth'] = True
                    response.set_cookie(PUNBB_COOKIE_NAME, pun_cookie)
            else:
                if punbb_authentified:
                    hash = md5.new('%d' % random.randint(0,1000)).hexdigest()
                    pun_cookie = PUNCOOKIE_TPL % (1, 1, hash)
                    request.session['punbb_auth'] = False
                    response.set_cookie(PUNBB_COOKIE_NAME, pun_cookie)
        except Exception:
            response.delete_cookie(PUNBB_COOKIE_NAME)
        
        return response
