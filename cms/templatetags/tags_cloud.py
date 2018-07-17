from django import template
from ..tagtools.tagcloud import TaggitCloud
from django.conf import settings

from ..models import TextPost, BinaryPost

register = template.Library()

@register.assignment_tag(takes_context=False)
def tags_cloud():
  cloud_calculator = TaggitCloud([TextPost, BinaryPost], getattr(settings, 'TAGTOOLS_CLOUD_STEPS', 6), getattr(settings, 'TAGTOOLS_CLOUD_MIN_COUNT', 1))

  print(cloud_calculator)

  return cloud_calculator.calculate_cloud()