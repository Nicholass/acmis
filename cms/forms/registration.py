from django import forms
from django.utils.translation import ugettext as _
from captcha.fields import ReCaptchaField

from .. import validators

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from ..models import EmailChange



class RegistrationForm(UserCreationForm):
  captcha = ReCaptchaField()

  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators=[validators.reserved_name, validators.validate_confusables]
    self.fields['email'].validators=[validators.validate_confusables_email, validators.free_email]
    self.fields['email'].required = True
    self.fields['captcha'].label = _('Captcha')

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      self.add_error('email', forms.ValidationError(_('User with this e-mail already exists')))

    return email


class RememberAuthenticationForm(AuthenticationForm):
  remember = forms.BooleanField(label=_('Remember me'), required=False)


class EmailChangeForm(forms.ModelForm):

  class Meta:
    model = EmailChange
    fields = ('new_email',)