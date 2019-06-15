from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class CmsPost(models.Model):
  author = models.ForeignKey('auth.User', verbose_name='Автор')
  title = models.CharField(max_length=200, verbose_name='Заголовок')
  category = models.ForeignKey('CmsCategory', blank=True, null=False, verbose_name='Категорія')

  text = RichTextField(verbose_name='Текст')

  tags = TaggableManager(blank=True, verbose_name='Тэги')
  created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата створення')
  modifed_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата редагування')
  is_permited = models.BooleanField(default=False, verbose_name='Зробити прихованим')

  def _tags(self):
        return [t.name for t in self.tags.all()]

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Пост'
    verbose_name_plural = 'Пости'
    permissions = (
        ('moderate_cmspost', 'Модерація постів'),
        ('permited_access', 'Доступ до прихованих постів'),
    )