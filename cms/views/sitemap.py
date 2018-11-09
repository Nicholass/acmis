from cms.models import CmsPost, CmsCategory
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class PostsSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return CmsPost.objects.filter(is_moderated=True, is_public=True, category__allow_anonymous=True)

  def lastmod(self, obj):
    return obj.created_date


class CategoriesSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return CmsCategory.objects.filter(allow_anonymous=True)

class StaticSitemap(Sitemap):
  priority = 0.6
  changefreq = 'never'

  def items(self):
    return ['pybb:index']

  def location(self, item):
    return reverse(item)
