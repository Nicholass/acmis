from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

def post_list(request, kind, category):
  posts = Post.objects.all()
  if kind:
    posts = posts.filter(kind = kind)
  if category:
    posts = posts.filter(category = category)

  return render(request, 'cms/post_list.html', {'posts': posts})

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'cms/post_detail.html', {'post': post})

def post_new(request, kind, category):
  if request.method == "POST":
    form = PostForm(request.POST)

    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.published_date = timezone.now()
      post.category = category
      post.kind = kind
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
