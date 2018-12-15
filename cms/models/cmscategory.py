from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import Group

class CmsCategory(models.Model):
  FILE = '0'
  POST = '1'
  UNKNOWN = '3'
  KINDS = (
    (FILE, _("File")),
    (POST, _("Post")),
    (UNKNOWN, _("Unknown")),
  )

  DATA_KINDS = {
    'drawing': FILE,
    'map': FILE,
    'news': POST,
    'photo': FILE,
    'prose': POST,
    'report': POST,
    'pm_report': POST
  }

  kind = models.CharField(
    max_length=254,
    null=False,
    blank=False,
    choices=KINDS,
    default=UNKNOWN,
    help_text=_('<font color="red">Attention! Changing this field in existing categories may affect the display of objects!</font>'),
    verbose_name=_("Type")
  )
  name = models.CharField(max_length=200, verbose_name=_("Name"))
  i18n_name = models.CharField(blank=True, null=True, max_length=200, verbose_name=_("i18n name"))
  i18n_name_plural = models.CharField(blank=True, null=True, max_length=200, verbose_name=_("i18n name plural"))
  route = models.CharField(
    max_length=200,
    verbose_name=_("Route"),
    help_text=_('<font color="red">Attention! Changing this field in existing categories may affect the logic!</font>'),
  )
  groups = models.ManyToManyField(Group, blank=True, verbose_name=_("Groups with access"))
  allow_anonymous = models.BooleanField(
    default=True,
    verbose_name=_("Full access"),
    help_text=_('Setting this checkbox disables access control to categories by user group.'),
  )

  def get_absolute_url(self):
    return "/category/%s/" % self.route

  def publish(self):
    self.kind = self.DATA_KINDS[self.route]
    #TODO: validate here
    self.save()

  def check_group_perm(self, user):
    if not user.is_authenticated() or user is None:
      return self.allow_anonymous

    return CmsCategory.objects.filter(pk=self.pk, groups__in=user.groups).exists()

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _("Category")
    verbose_name_plural = _("Categories")
