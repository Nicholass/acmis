from django import template

from cms.models.comment import Comment

register = template.Library()

@register.inclusion_tag("cms/last_comments.html", takes_context=False)
def last_comments(count = 10):
  comments = Comment.objects.filter(is_deleted=False).order_by('-created_date', '-id').select_related()
  comments_count = comments.count()

  if comments_count < count:
    count = comments_count
  elif comments_count == 0:
    return None

  comments = comments[:count]

  return {
    'comments': comments
  }
