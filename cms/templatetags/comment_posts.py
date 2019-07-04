from django import template
from django.db.models import Count

from cms.models.comment import Comment
from cms.models.cmspost import CmsPost

register = template.Library()

@register.inclusion_tag("cms/comment_posts.html", takes_context=False)
def comment_posts(count=10):
    comments = Comment.objects.filter(is_deleted=False).select_related().order_by('-created_date')
    comments_count = comments.count()

    if comments_count < count:
        count = comments_count
    elif comments_count == 0:
        return None

    comments = comments[:count]

    return {
        'comments': comments
    }
