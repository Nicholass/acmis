from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin

from cms.views.registration import send_activation_code
from cms.forms.profile import ProfileForm

from cms.models.cmspost import CmsPost
from cms.models.map import Map
from cms.models.cmscategory import CmsCategory
from cms.models.comment import Comment
from cms.models.cmsprofile import CmsProfile
from django.contrib.auth.models import User, Permission
from tracking.models import Visitor, Pageview

from .comment import CustomMPTTModelAdmin
from .post import PostAdmin
from .map import MapAdmin
from .tracking2 import PageviewCustomAdmin, VisitorCustomAdmin

admin.site.register(Comment, CustomMPTTModelAdmin)

admin.site.register(CmsPost, PostAdmin)
admin.site.register(Map, MapAdmin)

admin.site.unregister(Visitor)
admin.site.register(Visitor, VisitorCustomAdmin)

admin.site.unregister(Pageview)
admin.site.register(Pageview, PageviewCustomAdmin)


class CmsCategoryAdmin(admin.ModelAdmin):
    base_model = CmsCategory
    list_display = ('name', 'route')
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


class EmailVerefiedFilter(admin.SimpleListFilter):

    title = 'підтвержденням e-mail'
    parameter_name = 'email_verefied'

    def lookups(self, request, model_admin):
        return [(True, 'Так'), (False, 'Ні')]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(profile__email_verefied=self.value())

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_filter = ['is_active', 'is_staff', EmailVerefiedFilter, 'last_login']
    list_display = ('username', 'email', 'is_active', 'email_verefied', 'is_staff', 'last_login')
    actions = [send_activation,]

    def email_verefied(self, obj):
        return obj.profile.email_verefied
    email_verefied.boolean = True
    email_verefied.short_description = 'Пошту підтверджено'
    email_verefied.admin_order_field = 'profile__email_verefied'

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
