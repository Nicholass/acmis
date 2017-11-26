from django.contrib import admin
from .models import Post, TextPost, BinaryPost, Category
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from django import forms
from django.contrib.contenttypes.models import ContentType

class PostFormAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostFormAdmin, self).__init__(*args, **kwargs)

        # Limit category selection by post types
        post = kwargs.pop('instance', None)
        initial = kwargs.pop('initial', None)

        if post == None and initial == None:
            return
        elif post:
            kind = post.category.kind
        elif initial:
            ct_id = initial.pop('ct_id', None)
            ct = ContentType.objects.filter(id=ct_id).first()
            model = ct.model_class().__name__

            if model == 'BinaryPost':
              kind = '0'
            elif model == 'TextPost':
              kind = '1'
            else:
              kind = '3'

        self.fields['category'].queryset = Category.objects.filter(kind=kind)

class PostParentAdmin(PolymorphicParentModelAdmin):
    base_model = Post
    child_models = (TextPost, BinaryPost)
    list_filter = (PolymorphicChildModelFilter, 'created_date', 'tags')
    list_display = ('title', 'created_date', 'is_public', 'is_moderated', 'pk')
    date_hierarchy = 'created_date'
    ordering = ('-created_date', 'title',)
    search_fields = ['title']

class PostChildAdmin(PolymorphicChildModelAdmin):
    base_model = Post
    base_form = PostFormAdmin

admin.site.register(Post, PostParentAdmin)
admin.site.register(TextPost, PostChildAdmin)
admin.site.register(BinaryPost, PostChildAdmin)

class CategoryAdmin(admin.ModelAdmin):
    base_model = Category
    list_filter = ['kind']
    list_display = ('name', 'route', 'kind')
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
