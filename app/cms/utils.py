import re
import os
from django.utils.deconstruct import deconstructible
from uuid import uuid4
from PIL import Image

def clean_http(text):
    if not text:
      return None
    has_http = re.match(r'^(http://|https://)', text)
    if not has_http:
        text = "%s%s" % ('https://', text)
    return text

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

def is_owner(user, obj):
    model_name = obj.__class__.__name__.lower()

    is_moderator = user.has_perm('cms.moderate_%s' % model_name)
    is_owner = (obj.author == user)

    if is_owner or is_moderator:
        return True

    return False
