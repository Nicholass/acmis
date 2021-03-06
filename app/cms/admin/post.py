from django.contrib import admin

from cms.models.cmspost import CmsPost

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
            'js/jquery.min.js',
            'js/jquery-ui/jquery-ui.min.js',
            'js/jquery.tagsinput.min.js',
            'js/PostsForm.js'
        )
        css = {
            'screen': (
                'js/jquery-ui/jquery-ui.min.css',
                'js/jquery.tagsinput.min.css',
            ),
        }

    def get_short_title(self, obj):
        return obj.short_title

    get_short_title.short_description = 'Пост'
