import re
import os
from django.utils.deconstruct import deconstructible
from uuid import uuid4

def clean_http(text):
    if not text:
      return None
    has_http = re.match(r'^(http://|https://)', text)
    if not has_http:
        text = "%s%s" % ('https://', text)
    return text

def hide_first_item(text):
    items = re.search('(<p>)?((<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>))(</p>)?', text)
    if items:
        item = items.group(0)
        text = text.replace(item, '')
    return text

def get_post_announce(item):
    text = item.text

    items = re.search('(<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>)', text)
    if items:
        return items.group(0)

    return ''

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