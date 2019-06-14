import re
from django import forms

from ..models.cmspost import CmsPost


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['category'].required = True
        self.fields['text'].required = True
        self.fields['title'].required = True

    class Meta:
        model = CmsPost
        fields = ('title', 'text', 'category', 'tags')

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
