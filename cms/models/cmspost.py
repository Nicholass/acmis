from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class CmsPost(models.Model):
  author = models.ForeignKey('auth.User', verbose_name=_("Автор"))
  title = models.CharField(max_length=200, verbose_name=_("Название"))
  category = models.ForeignKey('CmsCategory', blank=True, null=False, verbose_name=_("Категория"))

  text = RichTextField(verbose_name=_("Text"))

  tags = TaggableManager(blank=True, verbose_name=_("Тэги"))
  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"))
  is_permited = models.BooleanField(default=False, verbose_name=_("Сделать закрытым"))

  def _tags(self):
        return [t.name for t in self.tags.all()]

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = _("Пост")
    verbose_name_plural = _("Посты")
    permissions = (
        ("moderate_cmspost", _("Модерация постов")),
        ("permited_access", _("Просмотр закрытых постов")),
    )