from datetime import timedelta
from django.contrib import admin


class VisitorCustomAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'

    list_display = ('session_key', 'user', 'start_time', 'session_over',
        'pretty_time_on_site', 'ip_address', 'user_agent')
    list_filter = ('user', 'ip_address')

    def session_over(self, obj):
        return obj.session_ended() or obj.session_expired()
    session_over.boolean = True

    def pretty_time_on_site(self, obj):
        if obj.time_on_site is not None:
            return timedelta(seconds=obj.time_on_site)
    pretty_time_on_site.short_description = 'Time on site'


class PageviewCustomAdmin(admin.ModelAdmin):
    date_hierarchy = 'view_time'

    def session_key(self, obj):
      return obj.visitor.session_key

    def user(self, obj):
      return obj.visitor.user

    def ip_address(self, obj):
      return obj.visitor.ip_address

    list_display = ('session_key', 'user', 'ip_address', 'url', 'referer', 'view_time')

