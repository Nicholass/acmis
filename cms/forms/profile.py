from django import forms
from django.utils.translation import ugettext as _
from django.core.files.images import get_image_dimensions
from django.conf import settings
import re
from pybb import defaults as pybb_defaults

from ..models import CmsProfile
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
  input_type = 'date'


class ProfileForm(forms.ModelForm):
  AVATAR_MAX_WIDTH = getattr(settings, 'AVATAR_MAX_WIDTH', '60')
  AVATAR_MAX_HEIGHT = getattr(settings, 'AVATAR_MAX_HEIGHT', '60')
  AVATAR_MAX_SIZE = getattr(settings, 'AVATAR_MAX_SIZE', '20')

  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)
    self.fields['avatar'].help_text = _('<ul><li>Avatar dimensions should be less than %(x)s x %(y)s px.</li><li>Avatar should be in format JPEG, GIF or PNG</li><li>Avatar size should be less than %(size)s Kb</li></ul>' % {'x': self.AVATAR_MAX_WIDTH, 'y': self.AVATAR_MAX_HEIGHT, 'size': self.AVATAR_MAX_SIZE})
    self.fields['signature'].widget = forms.Textarea(attrs={'rows': 2, 'cols:': 60})

  class Meta:
    model = CmsProfile
    fields = ('avatar', 'birth_date', 'location', 'site',  'skype', 'telegram', 'jabber', 'facebook', 'vk', 'instagram', 'twitter', 'youtube', 'signature', 'time_zone', 'language', 'show_signatures')
    widgets = {
      'birth_date': DateInput()
    }

  def clean_signature(self):
    value = self.cleaned_data['signature'].strip()
    if len(re.findall(r'\n', value)) > pybb_defaults.PYBB_SIGNATURE_MAX_LINES:
      raise forms.ValidationError('Number of lines is limited to %d' % pybb_defaults.PYBB_SIGNATURE_MAX_LINES)
    if len(value) > pybb_defaults.PYBB_SIGNATURE_MAX_LENGTH:
      raise forms.ValidationError('Length of signature is limited to %d' % pybb_defaults.PYBB_SIGNATURE_MAX_LENGTH)
    return value
  def clean_site(self):
    value = self.cleaned_data.get('site')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('http://', value)
    return value

  def clean_facebook(self):
    value = self.cleaned_data.get('facebook')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('https://', value)
    return value

  def clean_vk(self):
    value = self.cleaned_data.get('vk')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('https://', value)
    return value

  def clean_instagram(self):
    value = self.cleaned_data.get('instagram')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('https://', value)
    return value

  def clean_twitter(self):
    value = self.cleaned_data.get('twitter')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('https://', value)
    return value

  def clean_youtube(self):
    value = self.cleaned_data.get('youtube')
    if not value:
      return None
    has_http = re.match(r'^(http://|https://)', value)
    if not has_http:
      value = "%s%s" % ('https://', value)
    return value

  def clean_avatar(self):
    avatar = self.cleaned_data['avatar']

    if not avatar:
      return None

    try:
      w, h = get_image_dimensions(avatar)

      #validate dimensions
      if w > self.AVATAR_MAX_WIDTH or h > self.AVATAR_MAX_HEIGHT:
        raise forms.ValidationError(
          _('Avatar dimensions greater than %(x)s x %(y)s px' % {'x': self.AVATAR_MAX_WIDTH, 'y': self.AVATAR_MAX_HEIGHT})
        )

      #validate content type
      main, sub = avatar.content_type.split('/')
      if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
        raise forms.ValidationError(_('Avatar format is not JPEG, GIF or PNG'))

      #validate file size
      if len(avatar) > int(self.AVATAR_MAX_SIZE * 1024):
        raise forms.ValidationError(_('Avatar size greater than %s Kb' % self.AVATAR_MAX_SIZE ))

    except AttributeError:
      """
      Handles case when we are updating the user profile
      and do not supply a new avatar
      """
      pass

    return avatar

class UserForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(UserForm, self).__init__(*args, **kwargs)

  class Meta:
    model = User
    fields = ('first_name', 'last_name')