from cms.models.cmspost import CmsPost
from cms.models.cmscategory import CmsCategory
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class PostsSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return CmsPost.objects.all()

  def lastmod(self, obj):
    return obj.created_date


class CategoriesSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return CmsCategory.objects.all()

class StaticSitemap(Sitemap):
  priority = 0.6
  changefreq = 'never'

  def location(self, item):
    return reverse(item)
