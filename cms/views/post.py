from ..shortcuts import get_permited_object_or_403, is_owner_or_403, is_moderator_or_403
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from hashlib import md5

from ..forms import TextPostForm, BinaryPostForm, PostForm

from ..models import Post, Category


def post_list(request, tags=None, category=None, author=None, disapproved=None):

  t = c = None
  if not category and not tags and not author:
    category = getattr(settings, 'HOME_CATEGORY_ROUTE', 'news')

  if category:
    c = get_permited_object_or_403(Category, request.user, route=category)

  if tags:
    t = tags.split(",")

  query = {
    'tags__name__in': t,
    'author__username': author,
    'category': c,
    'is_moderated': True
  }

  q = {k: v for k, v in query.items() if v is not None}
  q_groups = { **q, 'category__groups__in': request.user.groups.all() }
  q_anoymous = { **q, 'category__allow_anonymous': True }

  posts_list = Post.objects.filter(Q(**q_anoymous) | Q(**q_groups)).distinct().order_by('-created_date', 'title')

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 'news'))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  if category == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps') and request.user.is_authenticated():
    for post in posts:
      for map_hash, pk in request.session['map_urls'].items():
        if post.pk == pk:
          post.hash = map_hash

  posts_disapproved = Post.objects.filter(category=c, is_moderated=False)

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'tags': t,
    'author': author,
    'posts_disapproved': len(posts_disapproved)
  })


def post_disapproved(request, category):
  c = get_permited_object_or_403(Category, request.user, route=category)
  is_moderator_or_403(request.user)

  posts_list = Post.objects.filter(category=c, is_moderated=False)

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 'news'))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  if category == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps') and request.user.is_authenticated():
    for post in posts:
      for map_hash, pk in request.session['map_urls'].items():
        if post.pk == pk:
          post.hash = map_hash

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'is_disapproved': True
  })

def post_detail(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)

  if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
    raise Http404("No Post matches the given query.")

  posts = Post.objects.filter(category=post.category).order_by('published_date')

  return render(request, 'cms/post_detail.html', {'post': post, 'posts': posts})


@login_required
@permission_required('cms.add_post', raise_exception=True)
def post_new(request,category):
  categoryObj = get_permited_object_or_403(Category, request.user, route=category)

  if categoryObj.kind == '0':
    formClass = BinaryPostForm
  elif categoryObj.kind == '1':
    formClass = TextPostForm
  else:
    formClass = PostForm

  if request.method == "POST":
    form = formClass(request.POST, request.FILES)

    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.published_date = timezone.now()
      post.category = categoryObj

      is_premod_cat = post.category.route in getattr(settings, 'PREMODERATION_CATEGORIES', [])
      is_premod_group = request.user.groups.filter(name__in=getattr(settings, 'PREMODERATION_GROUPS', [])).exists()

      if is_premod_cat and is_premod_group:
        post.is_moderated = False

      post.save()
      form.save_m2m()

      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        request.session['map_urls'][md5(str(post.pk).encode()).hexdigest()] = post.pk
        request.session.modified = True

      if is_premod_cat and is_premod_group:
        return render(request, 'cms/post_moderation.html', {'category':  post.category})

      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        return redirect('category_list', category=getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'))
      else:
        return redirect('post_detail', pk=post.pk)
  else:
    form = formClass()

  return render(request, 'cms/post_edit.html', {'form': form, 'category':  categoryObj})


@login_required
@permission_required('cms.change_post', raise_exception=True)
def post_edit(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)

  is_owner_or_403(request.user, post)

  if post.category.kind == '0':
    formClass = BinaryPostForm
  elif post.category.kind == '1':
    formClass = TextPostForm
  else:
    formClass = PostForm

  if request.method == "POST":
    form = formClass(request.POST, request.FILES, instance=post)

    if form.is_valid():
      post = form.save(commit=False)

      post.save()
      form.save_m2m()

      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        return redirect('category_list', category=getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'))
      else:
        return redirect('post_detail', pk=post.pk)
  else:
    form = formClass(instance=post)

  return render(request, 'cms/post_edit.html', {'form': form, 'post': post, 'category':  post.category})


@login_required
@permission_required('cms.delete_post', raise_exception=True)
def post_delete(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)

  is_owner_or_403(request.user, post)

  category = post.category.route

  if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
    map_hash = [key for key, value in request.session['map_urls'].items() if value == post.pk][0]
    del request.session['map_urls'][map_hash]
    request.session.modified = True

  post.delete()
  return redirect('category_list', category=category)

@login_required
@permission_required('cms.publish_post', raise_exception=True)
def post_publish(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  is_owner_or_403(request.user, post)

  post.is_public = True
  post.save()

  return redirect('category_list', category=post.category.route)

@login_required
@permission_required('cms.publish_post', raise_exception=True)
def post_unpublish(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  is_owner_or_403(request.user, post)

  post.is_public = False
  post.save()

  return redirect('category_list', category=post.category.route)

@login_required
@permission_required('cms.moderate_post', raise_exception=True)
def post_approve(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  is_moderator_or_403(request.user, post)

  post.is_moderated = True
  post.save()

  return redirect('category_list', category=post.category.route)
