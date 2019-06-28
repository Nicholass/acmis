import re
from django import forms

from ..models.map import Map

class MapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['file'].required = True
        self.fields['title'].required = True

    class Meta:
        model = Map
        fields = ('title', 'file', 'description', 'tags')
        widgets = {
            'file': forms.FileInput
        }

    class Media:
        js = (
            'js/jquery-ui/jquery-ui.min.js',
            'js/jquery.tagsinput.min.js',
            'js/PostsForm.js'
        )
        css = {
            'screen': (
                'js/jquery-ui/jquery-ui.min.css',
                'js/jquery.tagsinput.min.css',
            ),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        for i, tag in enumerate(tags):
            tags[i] = re.sub(r'[^\w\s\d\-_,]', '', tag).lower()

        return tags
