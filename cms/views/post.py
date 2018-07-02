from ..shortcuts import get_permited_object_or_403, is_owner_or_403, is_moderator_or_403
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from hashlib import md5
from ..tagtools.tagcloud import TaggitCloud
from django.utils.translation import ugettext as _
from hitcount.views import HitCountMixin

from ..forms import TextPostForm, BinaryPostForm, PostForm

from ..models import CmsPost, TextPost, BinaryPost, CmsCategory
from hitcount.models import HitCount
from tracking_analyzer.models import Tracker


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

  query = {
    'tags__name__in': t,
    'author__username': author,
    'category': c,
    'is_moderated': True
  }

  q = {k: v for k, v in query.items() if v is not None}
  q_groups = { **q, 'category__groups__in': request.user.groups.all() }
  q_anoymous = { **q, 'category__allow_anonymous': True }

  posts_list = CmsPost.objects.filter(Q(**q_anoymous) | Q(**q_groups)).distinct().order_by('-created_date', 'title')

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 'news'))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  need_relogin = False

  if request.user.is_authenticated():
    for post in posts:
      if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
        if request.session['map_urls']:
          for map_hash, pk in request.session['map_urls'].items():
            if post.pk == pk:
              post.hash = map_hash
        else:
          need_relogin = True

  posts_disapproved = CmsPost.objects.filter(category=c, is_moderated=False)

  cloud_calculator = TaggitCloud([TextPost, BinaryPost], getattr(settings, 'TAGTOOLS_CLOUD_STEPS', 6), getattr(settings, 'TAGTOOLS_CLOUD_MIN_COUNT', 1))
  tags_cloud = cloud_calculator.calculate_cloud()

  if is_home:
    page_title = _('Все посты')
  elif author:
    page_title = _('Материалы пользователя %s') % author
  elif c:
    page_title = c.name
  elif t:
    page_title = _('Материалы')

  if t:
    page_title = _('%s по тэгам') % page_title
    for tag in t:
      page_title = _('%s #%s') % (page_title, tag)

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'tags': t,
    'author': author,
    'posts_disapproved': len(posts_disapproved),
    'need_relogin': need_relogin,
    'is_home': is_home,
    'tags_cloud': tags_cloud,
    'page_title': page_title
  })


def post_disapproved(request, category):
  c = get_permited_object_or_403(CmsCategory, request.user, route=category)
  is_moderator_or_403(request.user)

  posts_list = CmsPost.objects.filter(category=c, is_moderated=False)

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
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

  if post.category.route == getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'):
    raise Http404("No CmsPost matches the given query.")

  hit_count = HitCount.objects.get_for_object(post)
  HitCountMixin.hit_count(request, hit_count)

  posts = CmsPost.objects.filter(category=post.category).order_by('created_date')

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
@permission_required('cms.change_cmspost', raise_exception=True)
def post_edit(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

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

  post.is_public = True
  post.save()

  return redirect('category_list', category=post.category.route)

@login_required
@permission_required('cms.publish_cmspost', raise_exception=True)
def post_unpublish(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
  is_owner_or_403(request.user, post)

  post.is_public = False
  post.save()

  return redirect('category_list', category=post.category.route)

@login_required
@permission_required('cms.moderate_cmspost', raise_exception=True)
def post_approve(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
  is_moderator_or_403(request.user, post)

  post.is_moderated = True
  post.save()

  return redirect('category_disapproved', category=post.category.route)
