from ..shortcuts import get_permited_object_or_403, is_owner_or_403, is_moderator_or_403
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from hitcount.views import HitCountMixin

from ..forms.post import PostForm

from ..models.cmspost import CmsPost
from ..models.cmscategory import CmsCategory
from django.contrib.auth.models import User
from hitcount.models import HitCount
from tracking_analyzer.models import Tracker


def post_list(request, tags=None, category=None, author=None):

  if getattr(settings, 'DEBUG') and request.user.is_authenticated == False:
    return render(request, 'unconstruction.html')

  t = c = None

  if category:
    c = get_object_or_404(CmsCategory, route=category)
    Tracker.objects.create_from_request(request, c)

  if tags:
    t = tags.split(",")

  if author:
    get_object_or_404(User, username=author)

  query = {
    'tags__name__in': t,
    'author__username': author,
    'category': c,
  }

  q = {k: v for k, v in query.items() if v is not None}

  posts_list = CmsPost.objects.filter(Q(**q)).distinct().order_by('-created_date')

  page = request.GET.get('page', 1)

  paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 25))
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  categories = CmsCategory.objects.all()

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'categories_list': categories,
    'tags': t,
    'author': author,
  })

def post_detail(request, pk):
  post = get_object_or_404(CmsPost, pk=pk)

  hit_count = HitCount.objects.get_for_object(post)
  HitCountMixin.hit_count(request, hit_count)

  Tracker.objects.create_from_request(request, post)

  return render(request, 'cms/post_detail.html', {'post': post})

@login_required
@permission_required('cms.add_cmspost', raise_exception=True)
def post_new(request):
  if request.method == "POST":
    form = PostForm(request.POST)

    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user

      post.save()
      form.save_m2m()

      return redirect('post_detail', pk=post.pk)

  else:
    form = PostForm()

  return render(request, 'cms/post_edit.html', {'form': form})


@login_required
@permission_required('cms.change_cmspost', raise_exception=True)
def post_edit(request, pk):
  post = get_object_or_404(CmsPost, pk=pk)

  is_owner_or_403(request.user, post)

  if request.method == "POST":
    form = PostForm(request.POST, request.FILES, instance=post)

    if form.is_valid():
      post = form.save(commit=False)

      post.save()
      form.save_m2m()

      return redirect('post_detail', pk=post.pk)

  else:
    form = PostForm(instance=post)

  return render(request, 'cms/post_edit.html', {'form': form, 'post': post})


@login_required
@permission_required('cms.delete_cmspost', raise_exception=True)
def post_delete(request, pk):
  post = get_object_or_404(CmsPost, pk=pk)

  is_owner_or_403(request.user, post)
  category = post.category.route

  post.delete()
  return redirect('category_list', category=category)