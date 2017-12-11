from django.shortcuts import render, redirect

#TODO: select one between two functions
from .shortcuts import get_permited_object_or_404, get_permited_object_or_403, is_owner_or_403
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .forms import TextPostForm, BinaryPostForm, PostForm, CommentForm, RegistrationForm, ProfileForm

#TODO move to user's part
from hashlib import md5
from django.contrib.auth.signals import user_logged_in
def do_stuff(sender, user, request, **kwargs):
  maps = Post.objects.filter(category__route = getattr(settings, 'MAPS_CATEGORY_ROUTE', 'maps'))

  request.session['map_urls'] = {md5(str(m.pk).encode()).hexdigest(): m.pk for m in maps}

user_logged_in.connect(do_stuff)

from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

def send_activation_code(user, request):
  current_site = get_current_site(request)
  site_name = current_site.name
  domain = current_site.domain

  subject = render_to_string('registration/activation_email_subject.txt')
  message = render_to_string('registration/activation_email.html', {
    'email': user.email,
    'domain': domain,
    'site_name': site_name,
    'protocol': 'https' if request.is_secure() else 'http',
    'user': user,
    'activation_key': signing.dumps(
      obj = getattr(user, user.USERNAME_FIELD),
      salt = getattr(settings, 'REGISTRATION_SALT', 'registration')
    ),
    'expiration_days': getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)
  })
  user.email_user(subject, message)
#end TODO

def post_list(request, tags=None, category=None, author=None):

  t = c = None
  if not category and not tags and not author:
    category = getattr(settings, 'HOME_CATEGORY_ROUTE', 'news')

  if category:
    c = get_permited_object_or_403(Category, request.user, route=category)

  if tags:
    t = tags.split(",")

  query = {
    'is_public': True,
    'tags__name__in': t,
    'author__username': author,
    'category': c
  }

  q = {k: v for k, v in query.items() if v is not None}
  q_groups = { **q, 'category__groups__in': request.user.groups.all() }
  q_anoymous = { **q, 'category__allow_anonymous': True }

  posts = Post.objects.filter(Q(**q_anoymous) | Q(**q_groups)).distinct().order_by('-created_date', 'title')

  return render(request, 'cms/post_list.html', {
    'posts': posts,
    'category': c,
    'tags': t,
    'author': author
  })

def post_detail(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  return render(request, 'cms/post_detail.html', {'post': post})

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

      post.save()
      form.save_m2m()
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
  post.delete()
  return redirect('category_list', category=category)

@login_required
@permission_required('cms.add_comment', raise_exception=True)
def comment_new(request, pk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)

  if request.method == "POST":
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.author = request.user
      comment.post = post
      comment.save()

      return get_comment_url(post.pk, comment.pk)

  return redirect('post_detail', pk=post.pk)

@login_required
@permission_required('cms.change_comment', raise_exception=True)
def comment_edit(request, pk, cpk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  edited_comment = get_permited_object_or_403(Comment, request.user, pk=cpk)

  is_owner_or_403(request.user, edited_comment)

  if request.method == "POST":
    form = CommentForm(request.POST, instance=edited_comment)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.modifed_date = timezone.now()
      comment.save()

      return get_comment_url(post.pk, comment.pk)
  else:
    form = CommentForm(instance=edited_comment)

  return render(request, 'cms/comment_edit.html', {'form': form, 'post': post, 'comment': edited_comment})

@login_required
@permission_required('cms.add_comment', raise_exception=True)
def comment_reply(request, pk, cpk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  parent = get_permited_object_or_403(Comment, request.user, pk=cpk)

  if request.method == "POST":
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.author = request.user
      comment.post = post
      comment.parent = parent
      comment.save()

      return get_comment_url(post.pk, comment.pk)
  else:
    form = CommentForm()

  return render(request, 'cms/comment_edit.html', {'form': form, 'post': post, 'parent': parent})

@login_required
@permission_required('cms.delete_comment', raise_exception=True)
def comment_delete(request, pk, cpk):
  post = get_permited_object_or_403(Post, request.user, pk=pk)
  comment = get_permited_object_or_403(Comment, request.user, pk=cpk)

  is_owner_or_403(request.user, comment)

  comment.is_deleted = True
  comment.save()

  return HttpResponseRedirect('%s#comments' % reverse('post_detail', kwargs={'pk':pk}))

def get_comment_url(pk, cpk):
  return HttpResponseRedirect('%s#comment%s' % (reverse('post_detail', kwargs={'pk':pk}), cpk))

def serve_map_file(request, map_hash):
  try:
    map_pk = request.session['map_urls'][map_hash]
    m = get_permited_object_or_403(Post, request.user, pk=map_pk)

    # import sys
    # for key, value in request.session.items(): print('{} => {}'.format(key, value), file=sys.stderr)

    return HttpResponse(m.file.file, content_type='image/jpg')
  except KeyError:
    raise Http404("No map found.")

def registration(request):
  if not getattr(settings, 'REGISTRATION_OPEN', True):
    return render(request, 'cms/registration/registration_closed.html')

  if request.method == 'POST':
    form = RegistrationForm(request.POST)

    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()

      send_activation(user)

      return render(request, 'registration/registration_complete.html')

  else:
    form = RegistrationForm()

  return render(request, 'registration/registration_form.html', {'form': form})

def activation(request, activation_key):
  try:
    username = signing.loads(
        activation_key,
        salt = getattr(settings, 'REGISTRATION_SALT', 'registration'),
        max_age = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2) * 86400
    )

    if username is not None:
      user = User.objects.get(**{
        User.USERNAME_FIELD: username,
        'is_active': False
      })

  # SignatureExpired is a subclass of BadSignature, so this will
  # catch either one.
  except (signing.BadSignature, User.DoesNotExist):
    user = None

  if user is not None:
    user.is_active = True
    user.save()

    return render(request, 'registration/activation_complete.html')

  return render(request, 'registration/activation_failed.html')