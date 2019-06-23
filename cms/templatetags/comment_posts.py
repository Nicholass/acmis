from django import template
from django.db.models import Count

from cms.models.cmspost import CmsPost

register = template.Library()


@register.inclusion_tag("cms/comment_posts.html", takes_context=False)
def comment_posts(count=10):
    posts = CmsPost.objects.annotate(comments_count=Count('comment')).order_by('-comments_count').select_related()
    posts_count = posts.count()

    if posts_count < count:
        count = posts_count
    elif posts_count == 0:
        return None

    posts = posts[:count]

    return {
        'posts': posts
    }
