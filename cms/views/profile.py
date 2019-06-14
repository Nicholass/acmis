from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..forms.profile import ProfileForm, UserForm

from django.contrib.auth.models import User

def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    context = {
        'profile_user': user,
        'base_path': settings.BASE_DIR,
    }

    return render(request, 'registration/profile.html', context)

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

            return redirect('profile', username=user.username)
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