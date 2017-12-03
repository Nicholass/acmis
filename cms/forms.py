from django import forms
from django.utils.translation import ugettext as _
from django.core.files.images import get_image_dimensions

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, TextPost, BinaryPost, Comment, Profile

from . import validators

class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ('title', 'tags', 'is_public')

class TextPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = TextPost
    fields = ('title', 'text', 'tags', 'is_public')

class BinaryPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = BinaryPost
    fields = ('title', 'file', 'description', 'tags', 'is_public')

class CommentForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':80}), label='')

  class Meta:
    fields = ('text',)
    model = Comment

class RegistrationForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators=[validators.reserved_name, validators.validate_confusables]
    self.fields['email'].validators=[validators.validate_confusables_email, validators.free_email]

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      self.add_error('email', forms.ValidationError(_('Пользователь с такими email уже существует')))

    return email

class ProfileForm(forms.ModelForm):
  AVATAR_MAX_WIDTH = 100
  AVATAR_MAX_HEIGHT = 100
  AVATAR_MAX_SIZE = 20

  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)
    self.fields['avatar'].help_text = _('<ul><li>Аватар не должен быть размером больше %s x %s пикселей.</li><li>Аватар должен быть изображением в формате JPEG, GIF или PNG</li><li>Аватар должен быть меньше %s Кб размером</li></ul>' % (self.AVATAR_MAX_WIDTH, self.AVATAR_MAX_HEIGHT, self.AVATAR_MAX_SIZE))
    self.fields['username'].validators=[validators.ReservedNameValidator, validators.validate_confusables]
    self.fields['email'].validators=[validators.validate_confusables_email]

  class Meta:
    model = Profile
    fields = ('avatar', 'birth_date', 'location', 'site',  'skype', 'telegram', 'jabber', 'facebook', 'vk', 'instagram', 'twitter', 'youtube')

  def clean_avatar(self):
    avatar = self.cleaned_data['avatar']

    if not avatar:
      return None

    try:
      w, h = get_image_dimensions(avatar)

      #validate dimensions
      max_width = max_height = 100
      if w > self.AVATAR_MAX_WIDTH or h > self.AVATAR_MAX_HEIGHT:
        raise forms.ValidationError(
          _('Аватар больше %s x %s пикселей размером' % (self.AVATAR_MAX_WIDTH, self.AVATAR_MAX_HEIGHT))
        )

      #validate content type
      main, sub = avatar.content_type.split('/')
      if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
        raise forms.ValidationError(_('Аватар не является изображением или не в форматах JPEG, GIF или PNG'))

      #validate file size
      if len(avatar) > (self.AVATAR_MAX_SIZE * 1024):
        raise forms.ValidationError(_('Аватар больше %s Кб размером' % self.AVATAR_MAX_SIZE ))

    except AttributeError:
      """
      Handles case when we are updating the user profile
      and do not supply a new avatar
      """
      pass

    return avatar