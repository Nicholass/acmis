import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def hide_announced(value):
    return re.sub('((<p>)?((<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>))(</p>)?)', '', value)

@register.assignment_tag(takes_context=False)
def get_announce(item):
    preview_items = re.search('(<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>)', item.short_text)
    if preview_items:
        return preview_items.group(0)

    items = re.search('(<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>)', item.text)

    if items:
        return items.group(0)

    return None
