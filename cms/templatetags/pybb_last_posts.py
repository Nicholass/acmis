from django import template
from django.core.urlresolvers import reverse

from pybb.models import Topic

register = template.Library()

@register.inclusion_tag("cms/pybb_last_posts.html", takes_context=False)
def pybb_last_posts(count = 10):
  last_posts  = []

  topics = Topic.objects.filter(forum__hidden=False).order_by('-updated', '-id')
  topics_count = topics.count()

  if topics_count < count:
    count = topics_count

  if topics_count == 0:
    return None

  topics = topics[:count]

  for top in topics:
    last_posts.append(top.last_post)

  if len(last_posts) == 0:
    return None

  return {
    'posts': last_posts
  }
