from django import forms
from django.utils.translation import ugettext as _
from django.core.files.images import get_image_dimensions
from django.conf import settings

from ..utils import clean_http

from ..models.cmsprofile import CmsProfile
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
  input_type = 'date'


class ProfileForm(forms.ModelForm):
  AVATAR_MAX_WIDTH = getattr(settings, 'AVATAR_MAX_WIDTH', '80')
  AVATAR_MAX_HEIGHT = getattr(settings, 'AVATAR_MAX_HEIGHT', '80')
  AVATAR_MAX_SIZE = getattr(settings, 'AVATAR_MAX_SIZE', '20')

  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)
    self.fields['avatar'].help_text = _('<ul><li>Avatar dimensions should be less than %(x)s x %(y)s px.</li><li>Avatar should be in format JPEG, GIF or PNG</li><li>Avatar size should be less than %(size)s Kb</li></ul>' % {'x': self.AVATAR_MAX_WIDTH, 'y': self.AVATAR_MAX_HEIGHT, 'size': self.AVATAR_MAX_SIZE})

  class Meta:
    model = CmsProfile
    fields = ('avatar', 'birth_date', 'location', 'skype', 'telegram', 'facebook', 'vk', 'instagram', 'twitter', 'youtube')
    widgets = {
      'birth_date': DateInput()
    }

  def clean_facebook(self):
    value = self.cleaned_data.get('facebook')
    return clean_http(value)

  def clean_vk(self):
    value = self.cleaned_data.get('vk')
    return clean_http(value)

  def clean_instagram(self):
    value = self.cleaned_data.get('instagram')
    return clean_http(value)

  def clean_twitter(self):
    value = self.cleaned_data.get('twitter')
    return clean_http(value)

  def clean_youtube(self):
    value = self.cleaned_data.get('youtube')
    return clean_http(value)

  def clean_avatar(self):
    avatar = self.cleaned_data['avatar']

    if not avatar:
      return False

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

class EmailChangeForm(forms.ModelForm):

  class Meta:
    model = CmsProfile
    fields = ('new_email',)