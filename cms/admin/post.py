from django import forms
from django.contrib.contenttypes.models import ContentType
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.utils.translation import ugettext as _

from ..models import Post, TextPost, BinaryPost, Category


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
  list_filter = (PolymorphicChildModelFilter, 'created_date', 'is_moderated', 'tags')
  list_display = ('get_short_title', 'category', 'created_date', 'author', 'is_public', 'is_moderated', 'pk')
  date_hierarchy = 'created_date'
  ordering = ('-created_date', 'title',)
  search_fields = ['title']

  def get_short_title(self, obj):
    return obj.short_title

  get_short_title.short_description = _('Пост')


class PostChildAdmin(PolymorphicChildModelAdmin):
  base_model = Post
  base_form = PostFormAdmin
