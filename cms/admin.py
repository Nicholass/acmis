from django.contrib import admin, messages
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext as _
from .views import send_activation_code

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from mptt.admin import MPTTModelAdmin

from .models import Post, TextPost, BinaryPost, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

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
    list_display = ('short_title', 'created_date', 'author', 'is_public', 'is_moderated', 'pk')
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

class ShortParentChoiseField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.short_text

class ShortPostChoiseField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.short_title

class CustomMPTTAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomMPTTAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'] = ShortParentChoiseField(queryset=Comment.objects.all(), label='Ответ на')
        self.fields['post'] = ShortPostChoiseField(queryset=Post.objects.all(), label='Пост')
        add_related_field_wrapper(self, 'parent')
        add_related_field_wrapper(self, 'post')

class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 10
    mptt_indent_field = 'short_text'
    list_filter = ['created_date', 'is_moderated']
    list_display = ('short_text', 'created_date', 'author', 'is_moderated', 'is_deleted', 'pk')
    date_hierarchy = 'created_date'
    search_fields = ['text']
    form = CustomMPTTAdminForm

admin.site.register(Comment, CustomMPTTModelAdmin)

def add_related_field_wrapper(form, col_name):
    rel_model = form.Meta.model
    rel = rel_model._meta.get_field(col_name).rel
    form.fields[col_name].widget = RelatedFieldWidgetWrapper(form.fields[col_name].widget, rel, admin.site, can_add_related=True, can_change_related=True)

def send_activation(modeladmin, request, queryset):
    for user in queryset:
        send_activation_code(user, request)

    messages.add_message(request, messages.INFO, _('Коды активации были отправлены выбранным аккаунтам'))

send_activation.short_description = _('Отправить код активации')

class UserAdminModel(UserAdmin):
    model = User
    list_filter = ['is_active', 'is_staff', 'last_login']
    list_display = ('username', 'email', 'is_active', 'is_staff', 'last_login')
    actions = [send_activation,]

admin.site.unregister(User)
admin.site.register(User, UserAdminModel)