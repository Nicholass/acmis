from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _
import re

from cms.models import CmsPost

class LatestEntriesFeed(Feed):
    title = _("Posts feed")
    link = "/"
    description = _('Last site posts')

    def items(self):
        return CmsPost.objects.filter(is_moderated=True, is_public=True, category__allow_anonymous=True).order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        tag_re = re.compile(r'<[^>]+>')

        if item.category.route == 'drawing' or item.category.route == 'photo':
          return tag_re.sub('', item.description)
        else:
          return tag_re.sub('', item.short_text)