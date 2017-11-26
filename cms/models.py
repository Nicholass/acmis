from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from taggit.managers import TaggableManager
from django.utils.translation import ugettext as _

class Post(PolymorphicModel):
  '''
  TODO:
  share post on save
  public/moderation part

  search and indexes

  comments
  '''

  author = models.ForeignKey('auth.User', verbose_name=_("Автор"))
  title = models.CharField(max_length=200, verbose_name=_("Название"))
  category = models.ForeignKey('Category', blank=True, null=False, verbose_name=_("Категория"))

  tags = TaggableManager(blank=True, verbose_name=_("Теги"))
  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"))
  published_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Дата публикации"))

  is_public = models.BooleanField(default=True, verbose_name=_("Опубликовано"))
  is_moderated = models.BooleanField(default=True, verbose_name=_("Одобрено модератором"))

  def _tags(self):
        return [t.name for t in self.tags.all()]

  def publish(self):
    '''
    TODO set is_public/is_moderated basing on category/etc
    '''
    self.published_date = timezone.now()

    self.save()

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = _("Пост")
    verbose_name_plural = _("Посты")

class TextPost(Post):
  text = models.TextField(verbose_name=_("Текст"))

  class Meta:
    verbose_name = _("Текстовый пост")
    verbose_name_plural = _("Текстовые посты")

class BinaryPost(Post):
  file = models.ImageField(
    blank=True,
    null=True,
    upload_to='uploads/%Y/%m/%d/',
    verbose_name=_("Файл")
  )
  description = models.CharField(max_length=200, verbose_name=_("Описание"))

  class Meta:
    verbose_name = _("Изображение")
    verbose_name_plural = _("Изображения")

class Category(models.Model):
  FILE = '0'
  POST = '1'
  UNKNOWN = '3'
  KINDS = (
    (FILE, _("Файлы")),
    (POST, _("Посты")),
    (UNKNOWN, _("Не определено")),
  )

  DATA_KINDS = {
    'Drawings': FILE,
    'Maps': FILE,
    'News': POST,
    'Photos': FILE,
    'Proses': POST,
    'Reports': POST
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
  route = models.CharField(max_length=200, verbose_name=_("Название в URL"))

  def publish(self):
    self.kind = self.DATA_KINDS[self.name]
    #TODO: validate here
    self.save()

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _("Категория")
    verbose_name_plural = _("Категории")