from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone

from ..shortcuts import get_permited_object_or_403, is_owner_or_403
from ..forms import CommentForm

from ..models import CmsPost, Comment


@login_required
@permission_required('cms.add_comment', raise_exception=True)
def comment_new(request, pk):
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)

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
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
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
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
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
  post = get_permited_object_or_403(CmsPost, request.user, pk=pk)
  comment = get_permited_object_or_403(Comment, request.user, pk=cpk)

  is_owner_or_403(request.user, comment)

  comment.is_deleted = True
  comment.save()

  return HttpResponseRedirect('%s#comments' % reverse('post_detail', kwargs={'pk':pk}))


def get_comment_url(pk, cpk):
  return HttpResponseRedirect('%s#comment%s' % (reverse('post_detail', kwargs={'pk':pk}), cpk))