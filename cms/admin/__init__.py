from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin

from ..views import send_activation_code

from ..models import Post, TextPost, BinaryPost, Category, Comment
from django.contrib.auth.models import User, Permission

from .comment import CustomMPTTModelAdmin
from .post import PostParentAdmin, PostChildAdmin

admin.site.register(Comment, CustomMPTTModelAdmin)

admin.site.register(Post, PostParentAdmin)
admin.site.register(TextPost, PostChildAdmin)
admin.site.register(BinaryPost, PostChildAdmin)


class CategoryAdmin(admin.ModelAdmin):
    base_model = Category
    list_filter = ['kind']
    filter_horizontal = ('groups', )
    list_display = ('name', 'route', 'kind', 'allow_anonymous')
    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)


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


class PermissionModel(admin.ModelAdmin):
    model = Permission
    list_filter = ['content_type']
    list_display = ('name', 'content_type', 'codename',)
    search_fields = ['name']
    ordering = ('name',)


admin.site.register(Permission, PermissionModel)