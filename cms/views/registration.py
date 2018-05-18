from django.shortcuts import render, redirect

from django.contrib.auth.views import login
from django.contrib.auth.models import User

from ..forms import RegistrationForm, EmailChangeForm

from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

def send_activation_code(user, request):
  current_site = get_current_site(request)
  site_name = current_site.name
  domain = current_site.domain

  subject = render_to_string('registration/activation_email_subject.txt')
  message = render_to_string('registration/activation_email.html', {
    'email': user.email,
    'domain': domain,
    'site_name': site_name,
    'protocol': 'https' if request.is_secure() else 'http',
    'user': user,
    'activation_key': signing.dumps(
      obj = getattr(user, user.USERNAME_FIELD),
      salt = getattr(settings, 'REGISTRATION_SALT', 'registration')
    ),
    'expiration_days': getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)
  })
  user.email_user(subject, message)

def registration(request):
  if not getattr(settings, 'REGISTRATION_OPEN', True):
    return render(request, 'registration/registration_closed.html')

  if request.method == 'POST':
    form = RegistrationForm(request.POST)

    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()

      send_activation_code(user, request)

      return render(request, 'registration/registration_complete.html')

  else:
    if 'proceed' not in request.GET:
      return render(request, 'registration/rules/{0}.html'.format(request.LANGUAGE_CODE))
    elif 'accept' not in request.GET:
      return redirect('post_list')

    form = RegistrationForm()

  return render(request, 'registration/registration_form.html', {'form': form})


def activation(request, activation_key):
  try:
    username = signing.loads(
        activation_key,
        salt = getattr(settings, 'REGISTRATION_SALT', 'registration'),
        max_age = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2) * 86400
    )

    if username is not None:
      user = User.objects.get(**{
        User.USERNAME_FIELD: username,
        'is_active': False
      })

  # SignatureExpired is a subclass of BadSignature, so this will
  # catch either one.
  except (signing.BadSignature, User.DoesNotExist):
    user = None

  if user is not None:
    user.is_active = True
    user.save()

    return render(request, 'registration/activation_complete.html')

  return render(request, 'registration/activation_failed.html')


def remember_login(request, *args, **kwargs):
  if request.method == 'POST':
    if not request.POST.get('remember', None):
      request.session.set_expiry(0)

  return login(request, *args, **kwargs)


def send_email_confirmation_code(user, token, request):
  current_site = get_current_site(request)
  site_name = current_site.name
  domain = current_site.domain

  subject = render_to_string('registration/email_change_subject.txt')
  message = render_to_string('registration/email_change_email.html', {
    'domain': domain,
    'site_name': site_name,
    'protocol': 'https' if request.is_secure() else 'http',
    'uid': user.pk,
    'token': token
  })
  user.email_user(subject, message)


def edit_email(request):
  if request.method == 'POST':
    form = EmailChangeForm(request.POST)

    if form.is_valid():
      new_email = form.save(commit=False)
      new_email.auth_key = '1234'
      new_email.user = request.user
      new_email.save()

      return render(request, 'registration/email_change_done.html')
  else:
    form = EmailChangeForm()

  return render(request, 'registration/email_change_form.html', {
    'form': form
  })