from hashlib import md5
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse, Http404
from django.conf import settings
import random

from ..shortcuts import get_permited_object_or_403

from ..models import CmsPost


def serve_map_file(request, map_hash):
  try:
    map_pk = request.session['map_urls'][map_hash]
    m = get_permited_object_or_403(CmsPost, request.user, pk=map_pk)

    # import sys
    # for key, value in request.session.items(): print('{} => {}'.format(key, value), file=sys.stderr)

    return HttpResponse(m.file.file, content_type='image/jpg')
  except KeyError:
    raise Http404("No map found.")


def do_stuff(sender, user, request, **kwargs):
  maps = CmsPost.objects.filter(category__route = getattr(settings, 'MAPS_CATEGORY_ROUTE', 'map'))
  request.session['map_urls'] = {md5(str(m.pk + random.randint(1, 32)).encode()).hexdigest(): m.pk for m in maps}


user_logged_in.connect(do_stuff)