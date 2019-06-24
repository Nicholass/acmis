from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Count

from cms.forms.profile import ProfileForm, UserForm

from django.contrib.auth.models import User
from cms.models.cmspost import CmsPost

def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    posts = CmsPost.objects.filter(author=user).distinct().order_by('-created_date')[0:30]

    return render(request, 'registration/profile.html', { 'user': user, 'posts': posts })

@login_required
@transaction.atomic
def profile_edit(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            if username:
                return redirect('profile', username=user.username)
            else:
                return redirect('me')

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    return render(request, 'registration/profile_edit.html', {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
    })

def userlist(request):
    users_list = User.objects.annotate(posts_count=Count('cmspost', distinct=True)).annotate(comments_count=Count('comment', distinct=True)).all().order_by('username')
    page = request.GET.get('page', 1)

    paginator = Paginator(users_list, getattr(settings, 'PAGINATION_USERS_COUNT', 25))
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'registration/users_list.html', { 'users': users })