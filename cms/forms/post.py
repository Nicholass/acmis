import re
from django import forms

from ..models import CmsPost, TextPost, BinaryPost


class PostForm(forms.ModelForm):

  class Meta:
    model = CmsPost
    fields = ('title', 'tags', 'is_public')

  class Media:
    js = (
      'jquery.tagsinput/src/jquery.tagsinput.js',
      'js/PostsForm.js'
    )
    css = {
      'screen': (
        'jquery.tagsinput/src/jquery.tagsinput.css',
      ),
    }

  def clean_tags(self):
    tags = self.cleaned_data.get('tags')

    for i, tag in enumerate(tags):
      tags[i] = re.sub(r'[^\w\s\d\-_,]', '', tag).lower()

    return tags

class TextPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = TextPost
    fields = ('title', 'text', 'tags', 'is_public')


class BinaryPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = BinaryPost
    fields = ('title', 'file', 'description', 'tags', 'is_public')
