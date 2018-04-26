from django import forms

from ..models import Comment


class CommentForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 80}), label='')

  class Meta:
    fields = ('text',)
    model = Comment
