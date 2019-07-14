from mptt.admin import MPTTModelAdmin
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib import admin

from ..models.comment import Comment
from ..models.cmspost import CmsPost


class ShortParentChoiseField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return obj.short_text


class ShortPostChoiseField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return obj.short_title


def add_related_field_wrapper(form, col_name):
  rel_model = form.Meta.model
  rel = rel_model._meta.get_field(col_name).rel
  form.fields[col_name].widget = RelatedFieldWidgetWrapper(form.fields[col_name].widget, rel, admin.site, can_add_related=True, can_change_related=True)


class CustomMPTTAdminForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(CustomMPTTAdminForm, self).__init__(*args, **kwargs)
    self.fields['parent'] = ShortParentChoiseField(queryset=Comment.objects.all(), label='Reply to')
    self.fields['parent'].required = False
    self.fields['post'] = ShortPostChoiseField(queryset=CmsPost.objects.all(), label='Post')
    add_related_field_wrapper(self, 'parent')
    add_related_field_wrapper(self, 'post')


class CustomMPTTModelAdmin(MPTTModelAdmin):
  # specify pixel amount for this ModelAdmin only:
  mptt_level_indent = 10
  mptt_indent_field = 'get_short_text'
  list_filter = ['created_date']
  list_display = ('get_short_text', 'get_post', 'created_date', 'author', 'is_deleted', 'pk')
  date_hierarchy = 'created_date'
  search_fields = ['text']
  form = CustomMPTTAdminForm

  def get_post(self, obj):
    return obj.post.short_title

  def get_short_text(self, obj):
    return obj.short_text

  get_short_text.short_description = 'Коментар'
  get_post.short_description = 'Пост'
