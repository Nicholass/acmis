from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

def post_list(request, tag='', category='', author=''):
  '''TODO posts.filter of get new list
  in case of complex situations like `/author|category/tag`

  posts = posts and posts.filter(%filter%) or get_list_or_404(post, %filter%)
  '''

  if tag:
    posts = get_list_or_404(Post, tags = tag) #FIXME
  elif category:
    posts = get_list_or_404(Post, category__route = category)
  elif author:
    posts = get_list_or_404(Post, author__username = author)
  else:
    posts = Post.objects.all()

  return render(request, 'cms/post_list.html', {'posts': posts})

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'cms/post_detail.html', {'post': post})

def post_new(request,category):
  if request.method == "POST":
    form = PostForm(request.POST)

    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.published_date = timezone.now()
      post.category = category
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm()
  return render(request, 'cms/post_edit.html', {'form': form})

def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm(instance=post)
  return render(request, 'cms/post_edit.html', {'form': form})
