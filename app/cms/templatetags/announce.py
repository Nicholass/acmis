from django import template
from cms.utils import get_post_announce, hide_first_item
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.assignment_tag(takes_context=False)
def get_announce(item):
    return get_post_announce(item)

@register.filter
@stringfilter
def hide_announced_item(value):
    return hide_first_item(value)
