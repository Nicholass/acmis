from django import template
from cms.forms.comment import CommentForm
from cms.models.comment import Comment
from cms.models.comment_unread import CommentUnread
from django.db.models import Exists, OuterRef

register = template.Library()

@register.inclusion_tag("cms/comment_form.html")
def comment_form(post):
    form = CommentForm()
    return {'form': form, 'post': post}

@register.inclusion_tag("cms/comment_list.html", takes_context=True)
def comment_list(context):
    post = context['post']
    user = context['user']

    if user.is_authenticated:
        unread_comment = CommentUnread.objects.filter(user=user, comment__pk=OuterRef('pk'))
        comments = Comment.objects.annotate(new=Exists(unread_comment)).filter(post=post)
    else:
        comments = Comment.objects.filter(post=post)

    return {
      'comments': comments,
      'post': post,
      'user': user,
      'perms': context['perms'],
    }

@register.assignment_tag(takes_context=True)
def clear_unread_comments(context):
    user = context['user']
    if user.is_authenticated:
        CommentUnread.objects.filter(user=user, post=context['post']).delete()

    return ''

@register.assignment_tag(takes_context=True)
def comment_count(context):
    return Comment.objects.filter(post=context['post']).count()

@register.assignment_tag(takes_context=True)
def new_comment_count(context):
    return CommentUnread.objects.filter(post=context['post'], user=context['user']).count()

@register.filter
def plural_type(value):
    digit = value % 10

    if digit == 1:
      return 1
    elif digit in [2, 3, 4]:
      return 2
    else:
      return 3