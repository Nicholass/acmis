from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _
from django.template.defaultfilters import truncatechars
import re

from cms.models.cmspost import CmsPost

class LatestEntriesFeed(Feed):
    title = _("Posts feed")
    link = "/"
    description = _('Last site posts')

    def items(self):
        return CmsPost.objects.all().order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', truncatechars(item.text, 400))
