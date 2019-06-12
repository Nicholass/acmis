from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..forms import ProfileForm, UserForm

from django.contrib.auth.models import User

def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    is_moderator = request.user.has_perm('cms.moderate_profile')
    is_owner = (request.user == user)

    context = {
        'profile_user': user,
        'is_owner': is_owner,
        'is_moderator': is_moderator,
        'base_path': settings.BASE_DIR,
    }

    return render(request, 'registration/profile.html', context)

@login_required
def owner_profile(request):
    user = request.user

    context = {
        'profile_user': user,
        'is_owner': True,
        'is_moderator': False,
        'base_path': settings.BASE_DIR
    }

    return render(request, 'registration/profile.html', context)


@login_required
@transaction.atomic
def profile_edit(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    is_moderator = request.user.has_perm('cms.moderate_profile')
    is_owner = (request.user == user)

    if not is_moderator and not is_owner:
        raise PermissionDenied()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('another_profile', username=user.username)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'registration/profile_edit.html', {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
    })

def userlist(request):
    users_list = User.objects.all().order_by('username')
    page = request.GET.get('page', 1)

    paginator = Paginator(users_list, getattr(settings, 'PAGINATION_USERS_COUNT', 25))
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'registration/users_list.html', {
      'users': users
    })