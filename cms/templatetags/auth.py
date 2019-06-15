from django import template
from cms.shortcuts import is_owner as own_check

register = template.Library()

@register.assignment_tag(takes_context=True)
def auth_is_owner(context, obj):
    return own_check(context['user'], obj)

