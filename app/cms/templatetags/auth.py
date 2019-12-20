from django import template
from cms.utils import is_owner

register = template.Library()

@register.assignment_tag(takes_context=True)
def auth_is_owner(context, obj):
    return is_owner(context['user'], obj)

