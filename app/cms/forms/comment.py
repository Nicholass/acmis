from django import forms

from cms.models.comment import Comment


class CommentForm(forms.ModelForm):

  class Meta:
    fields = ('text',)
    model = Comment
