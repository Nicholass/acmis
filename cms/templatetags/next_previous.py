from django import template

from ..utils import get_next_or_previous

register = template.Library()

"""
Efficient and generic get next/previous tags for the Django template language,
using Alex Gaynor's excellent templatetag_sugar library.
The library can be found at: http://pypi.python.org/pypi/django-templatetag-sugar
Usage:
    {% load next_previous %}
    ...
    {% get_next in <queryset> after <object> as <next> %}
    {% get_previous in <queryset> before <object> as <previous> %}
"""


@register.assignment_tag(takes_context=False)
def get_next(queryset, item):
  return get_next_or_previous(queryset, item, next=True)



@register.assignment_tag(takes_context=False)
def get_previous(queryset, item):
  return get_next_or_previous(queryset, item, next=False)