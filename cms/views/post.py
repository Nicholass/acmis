from ..shortcuts import get_permited_object_or_403, is_owner_or_403, is_moderator_or_403
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from hashlib import md5
from django.utils.translation import ugettext as _
from hitcount.views import HitCountMixin
from ..utils import i18n_grep
from .map import do_stuff
import random

from ..forms import TextPostForm, BinaryPostForm, PostForm

from ..models import CmsPost, CmsCategory
from hitcount.models import HitCount
from tracking_analyzer.models import Tracker
from django.contrib.auth.models import User


def post_list(request, tags=None, category=None, author=None):

  if getattr(settings, 'DEBUG') and request.user.is_authenticated == False:
    return render(request, 'unconstruction.html')

  t = c = None
  is_home = False

  if not category and not tags and not author:
    is_home = True

    home_category = getattr(settings, 'HOME_CATEGORY_ROUTE', False)
    if home_category:
      category = home_category

  if category:
    c = get_permited_object_or_403(CmsCategory, request.user, route=category)
    Tracker.objects.create_from_request(request, c)

  if tags:
    t = tags.split(",")

  if author:
    get_object_or_404(User, username=author)

  query = {
    'tags__name__in': t,
    'author__username': author,
    'category': c,
    'is_moderated': True,
    'is_public': True
  }

  q = {k: v for k, v in query.items() if v is not None}
  q_groups = { **q, 'category__groups__in': request.user.groups.all() }
  q_anoymous = { **q, 'category__allow_anonymous': True }

  posts_list = CmsPost.objects.filter(Q(**q_anoymous) | Q(**q_groups)).distinct().order_by('-publish_date', 'title')

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 25))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  if request.user.is_authenticated():
    for post in posts:
      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        if 'map_urls' not in request.session or not request.session['map_urls']:
          do_stuff(None, None, request)

        for map_hash, pk in request.session['map_urls'].items():
          if post.pk == pk:
            post.hash = map_hash

        if not hasattr(post, 'hash'):
          post.hash = md5(str(post.pk + random.randint(1, 32)).encode()).hexdigest()
          request.session['map_urls'][post.hash] = post.pk

  posts_disapproved_count = CmsPost.objects.filter(category=c, is_moderated=False, is_public=True).count()

  draft_query = {
    'category': c,
    'is_public': False,
    'author': None
  }

  if not request.user.is_anonymous():
    draft_query['author'] = request.user

  draft_filter = {k: v for k, v in draft_query.items() if v is not None}

  posts_draft_count = CmsPost.objects.filter(**draft_filter).count()

  if is_home:
    page_title = _('All posts')
  elif author:
    page_title = _('Posts of user: %s') % author
  elif c:
    if c.i18n_name:
      page_title = i18n_grep(c.i18n_name)
    else:
      page_title = c.name
  elif t:
    page_title = _('Posts')

  if t:
    page_title = _('%s by tags') % page_title
    for tag in t:
      page_title = _('%(title)s #%(tag)s') % {"title": page_title, "tag": tag}

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'tags': t,
    'author': author,
    'posts_disapproved': posts_disapproved_count,
    'posts_draft': posts_draft_count,
    'is_home': is_home,
    'page_title': page_title
  })

def post_disapproved(request, category):
  c = get_permited_object_or_403(CmsCategory, request.user, route=category)
  is_moderator_or_403(request.user)

  posts_list = CmsPost.objects.filter(category=c, is_moderated=False, is_public=True).order_by('-created_date', 'title')

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

def post_drafts(request, category):
  c = get_permited_object_or_403(CmsCategory, request.user, route=category)

  draft_query = {
    'category': c,
    'is_public': False,
    'author': None
  }

  if not request.user.is_anonymous():
    draft_query['author'] = request.user

  draft_filter = {k: v for k, v in draft_query.items() if v is not None}

  posts_list = CmsPost.objects.filter(**draft_filter).order_by('-created_date', 'title')

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 'news'))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  for post in posts:
    if post.category == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps') and request.user.is_authenticated():
      for map_hash, pk in request.session['map_urls'].items():
        if post.pk == pk:
          post.hash = map_hash

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'is_draft': True
  })

def post_detail(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

  if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
    raise Http404("No CmsPost matches the given query.")

  hit_count = HitCount.objects.get_for_object(post)
  HitCountMixin.hit_count(request, hit_count)

  posts = None

  if post.is_public and post.is_moderated:
    posts = CmsPost.objects.filter(is_public=True, is_moderated=True).order_by('publish_date')
    Tracker.objects.create_from_request(request, post)

  return render(request, 'cms/post_detail.html', {'post': post, 'posts': posts})


@login_required
@permission_required('cms.add_cmspost', raise_exception=True)
def post_new(request,category):
  categoryObj = get_permited_object_or_403(CmsCategory, request.user, route=category)

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
      post.category = categoryObj

      is_premod_cat = post.category.route in getattr(settings, 'PREMODERATION_CATEGORIES', [])
      is_premod_group = request.user.groups.filter(name__in=getattr(settings, 'PREMODERATION_GROUPS', [])).exists()

      if is_premod_cat and is_premod_group:
        post.is_moderated = False

      if post.is_moderated and post.is_public:
        post.publish_date = timezone.now()

      post.save()
      form.save_m2m()

      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        request.session['map_urls'][md5(str(post.pk).encode()).hexdigest()] = post.pk
        request.session.modified = True

      if not post.is_public:
        return render(request, 'cms/post_draft.html', {'category': post.category})

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
@permission_required('cms.change_cmspost', raise_exception=True)
def post_edit(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

  is_premod_cat = post.category.route in getattr(settings, 'PREMODERATION_CATEGORIES', [])
  is_premod_group = request.user.groups.filter(name__in=getattr(settings, 'PREMODERATION_GROUPS', [])).exists()

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

      if post.is_moderated and post.is_public and not post.publish_date:
        post.publish_date = timezone.now()

      if not post.is_public:
        post.publish_date = None

      post.save()
      form.save_m2m()

      if is_premod_cat and is_premod_group and not post.is_moderated:
        return render(request, 'cms/post_moderation.html', {'category':  post.category})

      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        return redirect('category_list', category=getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'))
      else:
        return redirect('post_detail', pk=post.pk)
  else:
    form = formClass(instance=post)

  return render(request, 'cms/post_edit.html', {'form': form, 'post': post, 'category':  post.category})


@login_required
@permission_required('cms.delete_cmspost', raise_exception=True)
def post_delete(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

  is_owner_or_403(request.user, post)

  category = post.category.route

  if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
    map_hash = [key for key, value in request.session['map_urls'].items() if value == post.pk][0]
    del request.session['map_urls'][map_hash]
    request.session.modified = True

  post.delete()
  return redirect('category_list', category=category)

@login_required
@permission_required('cms.publish_cmspost', raise_exception=True)
def post_publish(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
  is_owner_or_403(request.user, post)

  is_premod_cat = post.category.route in getattr(settings, 'PREMODERATION_CATEGORIES', [])
  is_premod_group = request.user.groups.filter(name__in=getattr(settings, 'PREMODERATION_GROUPS', [])).exists()

  post.is_public = True
  if post.is_moderated:
    post.publish_date = timezone.now()

  post.save()

  if is_premod_cat and is_premod_group and not post.is_moderated:
    return render(request, 'cms/post_moderation.html', {'category': post.category})

  return redirect('category_list', category=post.category.route)

@login_required
@permission_required('cms.moderate_cmspost', raise_exception=True)
def post_approve(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
  is_moderator_or_403(request.user, post)

  post.is_moderated = True
  post.publish_date = timezone.now()

  post.save()

  return redirect('category_disapproved', category=post.category.route)
