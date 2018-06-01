from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin

from ..views import send_activation_code
from ..forms import ProfileForm

from ..models import CmsPost, TextPost, BinaryPost, CmsCategory, Comment, CmsProfile, EmailChange
from django.contrib.auth.models import User, Permission

from .comment import CustomMPTTModelAdmin
from .post import PostParentAdmin, PostChildAdmin

admin.site.register(Comment, CustomMPTTModelAdmin)

admin.site.register(CmsPost, PostParentAdmin)
admin.site.register(TextPost, PostChildAdmin)
admin.site.register(BinaryPost, PostChildAdmin)


class CmsCategoryAdmin(admin.ModelAdmin):
    base_model = CmsCategory
    list_filter = ['kind']
    filter_horizontal = ('groups', )
    list_display = ('name', 'route', 'kind', 'allow_anonymous')
    ordering = ('name',)


admin.site.register(CmsCategory, CmsCategoryAdmin)


def send_activation(modeladmin, request, queryset):
    for user in queryset:
        send_activation_code(user, request)

    messages.add_message(request, messages.INFO, _('Коды активации были отправлены выбранным аккаунтам'))


send_activation.short_description = _('Отправить код активации')


class ProfileInline(admin.StackedInline):
    model = CmsProfile
    can_delete = False
    form = ProfileForm
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_filter = ['is_active', 'is_staff', 'last_login']
    list_display = ('username', 'email', 'is_active', 'is_staff', 'last_login')
    actions = [send_activation,]

    def __init__(self, *args, **kwargs):
      super(CustomUserAdmin, self).__init__(*args, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class PermissionModel(admin.ModelAdmin):
    model = Permission
    list_filter = ['content_type']
    list_display = ('name', 'content_type', 'codename',)
    search_fields = ['name']
    ordering = ('name',)


admin.site.register(Permission, PermissionModel)


class EmailChangeModel(admin.ModelAdmin):
    model = EmailChange
    list_display = ('new_email', 'user')
    search_fields = ['user']
    ordering = ('user',)


admin.site.register(EmailChange, EmailChangeModel)