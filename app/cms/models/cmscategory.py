from django.db import models


class CmsCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    route = models.CharField(
        max_length=200,
        verbose_name='Шлях',
    )

    def get_absolute_url(self):
        return '/category/%s/' % self.route

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
