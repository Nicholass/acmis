from django.shortcuts import render, redirect

from django.contrib.auth import views, login
from django.contrib.auth.models import User

from cms.forms.registration import RegistrationForm
from cms.forms.profile import EmailChangeForm
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail


def send_activation_code(user, request):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    subject = render_to_string('registration/activation_email_subject.txt')
    message = render_to_string('registration/activation_email.html', {
        'email': user.email,
        'domain': domain,
        'site_name': site_name,
        'user': user,
        'activation_key': signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=getattr(settings, 'REGISTRATION_SALT', 'registration')
        ),
        'expiration_days': getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)
    })
    user.email_user(subject, message)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_activation_code(user, request)

            return render(request, 'registration/registration_complete.html')

    else:
        form = RegistrationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


def activation(request, activation_key):
    user = None

    try:
        username = signing.loads(
            activation_key,
            salt=getattr(settings, 'REGISTRATION_SALT', 'registration'),
            max_age=getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2) * 86400
        )

        if username is not None:
            user = User.objects.get(**{
                User.USERNAME_FIELD: username
            })

    # SignatureExpired is a subclass of BadSignature, so this will
    # catch either one.
    except (signing.BadSignature, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.profile.email_verified = True
        user.save()

        return redirect('post_list')

    return render(request, 'registration/activation_failed.html')


def remember_login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)

    return views.login(request, *args, **kwargs)


def send_email_confirmation_code(user, token, email, request):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    subject = render_to_string('registration/email_change_subject.txt')
    message = render_to_string('registration/email_change_email.html', {
        'domain': domain,
        'site_name': site_name,
        'protocol': 'https' if request.is_secure() else 'http',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token
    })
    send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL'), [email])


@login_required
def edit_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)

        if form.is_valid():
            user = request.user
            user.profile.new_email = form.cleaned_data['new_email']
            user.profile.email_change_token = default_token_generator.make_token(request.user)
            user.save()

            send_email_confirmation_code(request.user, user.profile.email_change_token,  user.profile.new_email, request)

            return render(request, 'registration/email_change_done.html')
    else:
        form = EmailChangeForm()

    return render(request, 'registration/email_change_form.html', {
        'form': form
    })


def edit_email_done(request, uidb64, token):
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'registration/email_change_reject.html')

    if not default_token_generator.check_token(current_user, token):
        return render(request, 'registration/email_change_reject.html')

    current_user.email = current_user.profile.new_email
    current_user.profile.new_email = None
    current_user.save()

    return render(request, 'registration/email_change_confirm.html')
