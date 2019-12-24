import os
import wget
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import User

def download_avatar(url):
    filename, ext = (url.split('/')[-1].split('.'))
    file = '{}.{}'.format(uuid4().hex, ext)
    wget.download(url, os.path.join(getattr(settings, 'MEDIA_ROOT'), file))
    return file

def load_user(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
        print(kwargs['user'])
    except:
        pass
    return kwargs

def save_profile(backend, user, response, *args, **kwargs):
    print(user.username)
    print(backend.name)
    print(response)
    profile = user.profile

    if backend.name == 'google-oauth2':
        avatar_url = response.get('picture')
        if avatar_url and not profile.avatar:
            profile.avatar = download_avatar(avatar_url)

    if backend.name == 'facebook':
        avatar = response.get('picture')
        if avatar and not profile.avatar:
            profile.avatar = download_avatar(avatar.data.url)

        if not profile.facebook:
            profile.facebook = response.get('link')

        gender = response.get('gender')
        if gender and not profile.gender:
            if gender == 'male':
                profile.gender = 'BOY'
            elif gender == 'female':
                profile.gender = 'GIRL'
