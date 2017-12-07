from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Post, Category, Comment
from django.db.models import Q

'''
Example queries:

Post.objects.filter(pk=4, category__groups__in=user.groups.all())
Category.objects.filter(route='map', groups__in=user.groups.all())
Comment.objects.filter(pk=19, post__category__groups__in=user.groups.all())
'''

def get_permited_object_or_404(model, user, **kwargs):

  if model is Category:
    q_category_prefix = ''
  elif model is Post:
    q_category_prefix = 'category__'
  elif model is Comment:
    q_category_prefix = 'post__category__'

  q_groups = { **kwargs }
  q_anoymous = { **kwargs }

  q_groups['%sgroups__in' % q_category_prefix] = user.groups.all()
  q_anoymous['%sallow_anonymous' % q_category_prefix] = True

  return get_object_or_404(model, (Q(**q_anoymous) | Q(**q_groups)))

def get_permited_object_or_403(model, user, **kwargs):
  object = get_object_or_404(model, **kwargs)

  if model is Category:
    cat = object
  elif model is Post:
    cat = object.category
  elif model is Comment:
    cat = object.post.category

  if cat.allow_anonymous is not True:
    category_groups = cat.groups.all()
    user_groups = user.groups.all()

    if len(set(category_groups) & set(user_groups)) == 0:
      raise PermissionDenied()

  return object

def is_owner_or_403(user_obj, obj):
  if not is_owner(user_obj, obj):
    raise PermissionDenied()

def is_owner(user_obj, obj):
  model_name = obj.__class__.__name__.lower()

  is_moderator = user_obj.has_perm('cms.moderate_%s' % model_name)
  is_owner = (obj.author == user_obj)



  if is_owner or is_moderator:
    return True

  return False