from django import template
from ..utils import get_post_announce

register = template.Library()

@register.assignment_tag(takes_context=False)
def get_announce(item):
    return get_post_announce(item)