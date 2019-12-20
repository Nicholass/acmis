from django import template
from django.db.models import Q

from cms.models.cmspost import CmsPost

register = template.Library()

@register.inclusion_tag("cms/comment_posts.html", takes_context=False)
def comment_posts(count=10, user=None):
    query = {}

    if user and not user.has_perm('cms.permited_access'):
        query['is_permited'] = False

    posts = CmsPost.objects.filter(~Q(last_comment=None) & Q(**query)).order_by('-last_comment__created_date')
    posts_count = posts.count()

    if posts_count < count:
        count = posts_count
    elif posts_count == 0:
        return None

    posts = posts[:count]

    return {
        'posts': posts
    }
