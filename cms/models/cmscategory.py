from django.db import models
from django.utils.translation import ugettext as _

class CmsCategory(models.Model):
  name = models.CharField(max_length=200, verbose_name=_("Название"))
  route = models.CharField(
    max_length=200,
    verbose_name=_("Путь"),
  )

  def get_absolute_url(self):
    return "/category/%s/" % self.route

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _("Категория")
    verbose_name_plural = _("Категории")
