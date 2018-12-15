from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin
from pybb.admin import ForumAdmin

from ..views import send_activation_code
from ..forms import ProfileForm

from ..models import CmsPost, TextPost, BinaryPost, CmsCategory, Comment, CmsProfile, EmailChange, ForumGroups
from django.contrib.auth.models import User, Permission
from pybb.models import Forum
from tracking.models import Visitor, Pageview

from .comment import CustomMPTTModelAdmin
from .post import PostParentAdmin, PostChildAdmin
from .tracking2 import PageviewCustomAdmin, VisitorCustomAdmin

admin.site.register(Comment, CustomMPTTModelAdmin)

admin.site.register(CmsPost, PostParentAdmin)
admin.site.register(TextPost, PostChildAdmin)
admin.site.register(BinaryPost, PostChildAdmin)

admin.site.unregister(Visitor)
admin.site.register(Visitor, VisitorCustomAdmin)

admin.site.unregister(Pageview)
admin.site.register(Pageview, PageviewCustomAdmin)


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

    messages.add_message(request, messages.INFO, _('Activation codes sended to selected accounts'))


send_activation.short_description = _('Send activation code')


class ProfileInline(admin.StackedInline):
    model = CmsProfile
    can_delete = False
    form = ProfileForm
    verbose_name_plural = _('Profile')
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


class ForumGroupsInline(admin.StackedInline):
    model = ForumGroups
    can_delete = False
    verbose_name_plural = _('Forum groups')
    fk_name = 'forum'


class CustomForumAdmin(ForumAdmin):
    inlines = (ForumGroupsInline,)

    def __init__(self, *args, **kwargs):
        super(CustomForumAdmin, self).__init__(*args, **kwargs)


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomForumAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(Forum)
admin.site.register(Forum, CustomForumAdmin)

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