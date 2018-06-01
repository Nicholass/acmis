from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import Group

class CmsCategory(models.Model):
  FILE = '0'
  POST = '1'
  UNKNOWN = '3'
  KINDS = (
    (FILE, _("Файлы")),
    (POST, _("Посты")),
    (UNKNOWN, _("Не определено")),
  )

  DATA_KINDS = {
    'Drawing': FILE,
    'Map': FILE,
    'News': POST,
    'Photo': FILE,
    'Prose': POST,
    'Report': POST
  }

  kind = models.CharField(
    max_length=254,
    null=False,
    blank=False,
    choices=KINDS,
    default=UNKNOWN,
    help_text=_('<font color="red">Внимание! Изменение этого поля у существующих категорий может повлиять на отображение объектов!</font>'),
    verbose_name=_("Тип объектов")
  )
  name = models.CharField(max_length=200, verbose_name=_("Название"))
  route = models.CharField(
    max_length=200,
    verbose_name=_("Название в URL"),
    help_text=_('<font color="red">Внимание! Изменение этого поля у существующих категорий может повлиять на логику работы!</font>'),
  )
  groups = models.ManyToManyField(Group, blank=True, verbose_name=_("Группы имеющие доступ"))
  allow_anonymous = models.BooleanField(
    default=True,
    verbose_name=_("Полный доступ"),
    help_text=_('Установка этой галочки отключает контроль доступа к категории по группам пользователя'),
  )

  def publish(self):
    self.kind = self.DATA_KINDS[self.name]
    #TODO: validate here
    self.save()

  def check_group_perm(self, user):
    if not user.is_authenticated() or user is None:
      return self.allow_anonymous

    return CmsCategory.objects.filter(pk=self.pk, groups__in=user.groups).exists()

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _("Категория")
    verbose_name_plural = _("Категории")
