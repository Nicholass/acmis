from django import forms
from django.utils.translation import ugettext as _
from django.core.files.images import get_image_dimensions
from django.conf import settings

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
    self.fields['avatar'].help_text = _('<ul><li>Аватар не должен быть размером больше %s x %s пикселей.</li><li>Аватар должен быть изображением в формате JPEG, GIF или PNG</li><li>Аватар должен быть меньше %s Кб размером</li></ul>' % (self.AVATAR_MAX_WIDTH, self.AVATAR_MAX_HEIGHT, self.AVATAR_MAX_SIZE))

  class Meta:
    model = CmsProfile
    fields = ('avatar', 'birth_date', 'location', 'site',  'skype', 'telegram', 'jabber', 'facebook', 'vk', 'instagram', 'twitter', 'youtube')
    widgets = {
      'birth_date': DateInput()
    }

  def clean_avatar(self):
    avatar = self.cleaned_data['avatar']

    if not avatar:
      return None

    try:
      w, h = get_image_dimensions(avatar)

      #validate dimensions
      if w > self.AVATAR_MAX_WIDTH or h > self.AVATAR_MAX_HEIGHT:
        raise forms.ValidationError(
          _('Аватар больше %s x %s пикселей размером' % (self.AVATAR_MAX_WIDTH, self.AVATAR_MAX_HEIGHT))
        )

      #validate content type
      main, sub = avatar.content_type.split('/')
      if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
        raise forms.ValidationError(_('Аватар не является изображением или не в форматах JPEG, GIF или PNG'))

      #validate file size
      if len(avatar) > int(self.AVATAR_MAX_SIZE * 1024):
        raise forms.ValidationError(_('Аватар больше %s Кб размером' % self.AVATAR_MAX_SIZE ))

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