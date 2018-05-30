from django import forms

from ..models import Post, TextPost, BinaryPost


class PostForm(forms.ModelForm):

  class Meta:
    model = Post
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


class TextPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = TextPost
    fields = ('title', 'text', 'tags', 'is_public')


class BinaryPostForm(PostForm):

  class Meta(PostForm.Meta):
    model = BinaryPost
    fields = ('title', 'file', 'description', 'tags', 'is_public')
