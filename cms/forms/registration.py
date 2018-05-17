from django import forms
from django.utils.translation import ugettext as _

from .. import validators

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators=[validators.reserved_name, validators.validate_confusables]
    self.fields['email'].validators=[validators.validate_confusables_email, validators.free_email]
    self.fields['email'].required = True

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      self.add_error('email', forms.ValidationError(_('Пользователь с такими email уже существует')))

    return email


class RememberAuthenticationForm(AuthenticationForm):
  remember = forms.BooleanField(label=_('Запомнить меня'), required=False)