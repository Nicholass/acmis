import bleach

from urllib.parse import urlparse
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()

def allow_src(tag, name, value):
  if name == 'src':
    p = urlparse(value)
    return p.netloc in getattr(settings, 'BLEACH_ALLOWED_IFRAME_SRC', [])
  elif name in ['allowfullscreen', 'frameborder', 'height', 'width']:
    return True
  return False

@register.filter
@stringfilter
def bleach_src(value):
    return bleach.clean(
       value,
        tags=getattr(settings, 'BLEACH_ALLOWED_TAGS', []),
      attributes={
        'iframe': allow_src,
        '*': getattr(settings, 'BLEACH_ALLOWED_ATTRIBUTES', []),
      },
      styles=getattr(settings, 'BLEACH_ALLOWED_STYLES', []),
      strip=getattr(settings, 'BLEACH_STRIP_TAGS', False),
      strip_comments=getattr(settings, 'BLEACH_STRIP_COMMENTS', False),
    )