from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.utils.translation import ugettext as _
from simplemde.fields import SimpleMDEField


class Comment(MPTTModel):
    post = models.ForeignKey('CmsPost', on_delete=models.CASCADE, verbose_name=_("Пост"))
    author = models.ForeignKey('auth.User', verbose_name=_("Автор"))
    text = SimpleMDEField(verbose_name=_("Текст"))

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name=_("Ответ на"))

    is_moderated = models.BooleanField(default=True, verbose_name=_("Подтвержден модератором"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Удален"))

    created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"), unique=True)
    modifed_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата редактирования"))

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
