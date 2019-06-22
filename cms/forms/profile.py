from django import forms
from django.conf import settings

from ..utils import clean_http

from ..models.cmsprofile import CmsProfile
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    AVATAR_WIDTH = getattr(settings, 'AVATAR_WIDTH', '80')
    AVATAR_HEIGHT = getattr(settings, 'AVATAR_HEIGHT', '80')
    AVATAR_MAX_SIZE = getattr(settings, 'AVATAR_MAX_SIZE', '20')

    def __init__(self, *args, **kwargs):
      super(ProfileForm, self).__init__(*args, **kwargs)
      self.fields['avatar'].help_text = ('<ul><li>Аватар повинен будти у форматі JPEG, GIF або PNG</li>'
                                      '<li>Аватар повинен бути менше за %(size)s Kб</li></ul>' % {'size': self.AVATAR_MAX_SIZE})

    class Meta:
        model = CmsProfile
        fields = (
        'avatar', 'birth_date', 'gender', 'location', 'skype', 'telegram', 'facebook', 'vk', 'instagram', 'twitter',
        'youtube')
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
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
                raise forms.ValidationError('Аватар не є файлом JPEG, GIF або PNG')

            #validate file size
            if len(avatar) > int(self.AVATAR_MAX_SIZE * 1024):
              raise forms.ValidationError('Об\'єм аватара перевищує %s Kб' % self.AVATAR_MAX_SIZE )

        except AttributeError:
          """
          Handles case when we are updating the user profile
          and do not supply a new avatar
          """
          pass

        return avatar


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class EmailChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super(EmailChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CmsProfile
        fields = ('new_email',)

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']

        existing_user = User.objects.filter(email=new_email)
        if existing_user:
            raise forms.ValidationError('Користувач з таким e-mail вже існує')

        return new_email
