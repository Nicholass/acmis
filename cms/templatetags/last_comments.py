from django import template
from django.core.urlresolvers import reverse

from cms.models import Comment

register = template.Library()

@register.inclusion_tag("cms/last_comments.html", takes_context=False)
def last_comments(count = 10):
  comments = Comment.objects.filter(comments__post__category_allow_anonymous=True).order_by('-created_date', '-id').select_related('author')
  comments_count= comments.count()

  if comments_count < count:
    count = comments_count
  elif comments_count == 0:
    return None

  comments = comments[:count]

  return {
    'comments': comments
  }
