from django import template
from cms.shortcuts import is_owner as own_check, allow_view_category

register = template.Library()

@register.assignment_tag(takes_context=True)
def auth_is_owner(context, obj):
    return own_check(context['user'], obj)

@register.assignment_tag(takes_context=True)
def auth_can_view_category(context, category):
    return allow_view_category(context['user'], category)

