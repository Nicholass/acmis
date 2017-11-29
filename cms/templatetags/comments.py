from django import template
from cms.forms import CommentForm
from cms.models import Comment

register = template.Library()

@register.inclusion_tag("cms/comment_form.html")
def comment_form(post):
    form = CommentForm();
    return {'form': form, 'post': post}

@register.inclusion_tag("cms/comment_list.html", takes_context=True)
def comment_list(context):
    form = CommentForm()
    post = context['post']
    comments = Comment.objects.filter(post=post)
    return {
      'comments': comments,
      'post': post,
      'user': context['user']
    }

@register.simple_tag(takes_context=True)
def comment_count(context):
    return Comment.objects.filter(post=context['post']).count()

@register.filter
def plural_type(value):
    digit = value % 10

    if digit == 1:
      return 1
    elif digit in [2, 3, 4]:
      return 2
    else:
      return 3