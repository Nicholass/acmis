from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.assignment_tag(takes_context=False)
def pybb_last_posts():
  return '[items here]'
