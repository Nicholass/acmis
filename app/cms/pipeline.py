from __future__ import with_statement
import os
import wget
import contextlib
import datetime
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import User
from urllib.request import urlopen
from urllib.parse import urlencode

def download_avatar(url):
    file = '{}.{}'.format(uuid4().hex, 'jpg')
    wget.download(url, os.path.join(getattr(settings, 'MEDIA_ROOT'), file))
    return file

def make_tiny(url):
    request_url = ('https://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')

def load_user(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs

def save_profile(backend, user, response, *args, **kwargs):
    profile = user.profile
    profile.email_verefied = True

    if backend.name == 'google-oauth2':
        avatar_url = response.get('picture')
        if avatar_url and not profile.avatar:
            profile.avatar = download_avatar(avatar_url)

    if backend.name == 'facebook':
        avatar = response.get('picture')
        if avatar and not profile.avatar:
            profile.avatar = download_avatar(avatar['data']['url'])

        link = response.get('link')
        if link and not profile.facebook:
            profile.facebook = make_tiny(link)

        birthday = response.get('birthday')
        if birthday and not profile.birth_date:
            profile.birth_date = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')

        gender = response.get('gender')
        if gender and not profile.gender:
            if gender == 'male':
                profile.gender = 'BOY'
            elif gender == 'female':
                profile.gender = 'GIRL'

    profile.save()
