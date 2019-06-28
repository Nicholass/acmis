from django import template
from ..tagtools.tagcloud import TaggitCloud
from django.conf import settings

from cms.models.cmspost import CmsPost
from cms.models.map import Map

register = template.Library()

@register.assignment_tag(takes_context=False)
def tags_cloud():
  cloud_calculator = TaggitCloud([CmsPost], getattr(settings, 'TAGTOOLS_CLOUD_STEPS', 6), getattr(settings, 'TAGTOOLS_CLOUD_MIN_COUNT', 1))

  return cloud_calculator.calculate_cloud()

@register.assignment_tag(takes_context=False)
def maps_tags_cloud():
  cloud_calculator = TaggitCloud([Map], getattr(settings, 'TAGTOOLS_CLOUD_STEPS', 6), getattr(settings, 'TAGTOOLS_CLOUD_MIN_COUNT', 1))

  return cloud_calculator.calculate_cloud()