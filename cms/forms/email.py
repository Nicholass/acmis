from django import forms

from ..models import EmailChange

class EmailChangeForm(forms.ModelForm):

  class Meta:
    model = EmailChange
    fields = ('new_email',)