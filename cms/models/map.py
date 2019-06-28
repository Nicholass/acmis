from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse

class Map(models.Model):
    author = models.ForeignKey('auth.User', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    tags = TaggableManager(blank=True, verbose_name='Тэги')

    file = models.ImageField(
        upload_to='maps/',
        verbose_name='Файл'
    )
    description = models.TextField(max_length=200, verbose_name='Опис', blank=True)

    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата створення')
    modifed_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата редагування')

    @property
    def short_title(self):
        return truncatechars(self.title, 100)

    def _tags(self):
        return [t.name for t in self.tags.all()]

    def get_absolute_url(self):
        return reverse('map', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мапа'
        verbose_name_plural = 'Мапи'
        permissions = (
            ('moderate_cmspost', 'Модерація мап'),
            ('map_access', 'Доступ до мап'),
        )