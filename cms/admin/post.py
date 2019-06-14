from django.utils.translation import ugettext as _
from django.contrib import admin

from ..models.cmspost import CmsPost

class PostAdmin(admin.ModelAdmin):
    list_filter = ('created_date', 'tags')
    list_display = ('get_short_title', 'category', 'created_date', 'author', 'pk')
    date_hierarchy = 'created_date'
    ordering = ('-created_date', 'title',)
    search_fields = ['title']

    class Meta:
        model: CmsPost

    class Media:
        js = (
            'jquery/dist/jquery.min.js',
            'jquery-ui/jquery-ui.min.js',
            'jquery.tagsinput/src/jquery.tagsinput.js',
            'js/PostsForm.js'
        )
        css = {
            'screen': (
                'jquery-ui/themes/base/jquery-ui.min.css',
                'jquery.tagsinput/src/jquery.tagsinput.css',
            ),
        }

    def get_short_title(self, obj):
        return obj.short_title

    get_short_title.short_description = _('Post')
