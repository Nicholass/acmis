import re
from django import template
from django.template.defaultfilters import stringfilter
from ..utils import i18n_grep

register = template.Library()

@register.filter
@stringfilter
def i18n(value):
    return i18n_grep(value)