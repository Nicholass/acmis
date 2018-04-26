from django.db import models
from django.template.defaultfilters import truncatechars
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.utils.translation import ugettext as _


class Comment(MPTTModel):

  post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name=_("Пост"))
  author = models.ForeignKey('auth.User', verbose_name=_("Автор"))
  text = models.TextField(max_length=600, verbose_name=_("Текст"))

  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name=_("Ответ на"))

  is_moderated = models.BooleanField(default=True, verbose_name=_("Одобрен"))
  is_deleted = models.BooleanField(default=False, verbose_name=_("Удален"))

  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"), unique=True)
  modifed_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата редактирования"))

  @property
  def short_text(self):
    return truncatechars(self.text, 50)

  def __str__(self):
    return self.text

  class Meta:
    verbose_name = _("Комментарий")
    verbose_name_plural = _("Комментарии")
    permissions = (
        ("moderate_comment", _("Модерация комментариев")),
    )

  class MPTTMeta:
    order_insertion_by = ['created_date']
