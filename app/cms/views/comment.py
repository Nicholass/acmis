from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from cms.utils import is_owner
from django.shortcuts import get_object_or_404
from cms.forms.comment import CommentForm

from cms.models.cmspost import CmsPost
from cms.models.comment import Comment


@login_required
@permission_required('cms.add_comment', raise_exception=True)
def comment_new(request, pk):
    post = get_object_or_404(CmsPost, pk=pk)

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
    post = get_object_or_404(CmsPost, pk=pk)
    comment = get_object_or_404(Comment, pk=cpk)

    if not is_owner(request.user, comment):
        raise PermissionDenied()

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.modifed_date = timezone.now()
            comment.save()

            return get_comment_url(post.pk, comment.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'cms/comment_edit.html', {'form': form})


@login_required
@permission_required('cms.add_comment', raise_exception=True)
def comment_reply(request, pk, cpk):
    post = get_object_or_404(CmsPost, pk=pk)
    parent = get_object_or_404(Comment, pk=cpk)

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

    return render(request, 'cms/comment_edit.html', {'form': form, 'parent': parent})


@login_required
@permission_required('cms.delete_comment', raise_exception=True)
def comment_delete(request, pk, cpk):
    comment = get_object_or_404(Comment, pk=cpk)

    if not is_owner(request.user, comment):
        raise PermissionDenied()

    comment.is_deleted = True
    comment.save()

    return HttpResponseRedirect('%s#comments' % reverse('post_detail', kwargs={'pk': pk}))


def get_comment_url(pk, cpk):
    return HttpResponseRedirect('%s#comment%s' % (reverse('post_detail', kwargs={'pk': pk}), cpk))
