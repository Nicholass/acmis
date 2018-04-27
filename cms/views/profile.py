from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

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
        'user': user,
        'is_owner': is_owner,
        'is_moderator': is_moderator
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
        'user_form': user_form,
        'profile_form': profile_form
    })
