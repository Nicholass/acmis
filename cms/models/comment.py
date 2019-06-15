from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from simplemde.fields import SimpleMDEField


class Comment(MPTTModel):
    post = models.ForeignKey('CmsPost', on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey('auth.User', verbose_name='Автор')
    text = SimpleMDEField(verbose_name='Текст')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name='Відповідь на')

    is_deleted = models.BooleanField(default=False, verbose_name='Видалено')

    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата створення', unique=True)
    modifed_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата редагування')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        permissions = (
            ('moderate_comment', 'Модерація коментарів'),
        )

    class MPTTMeta:
        order_insertion_by = ['created_date']
