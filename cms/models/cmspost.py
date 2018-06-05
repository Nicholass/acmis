import os

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from polymorphic.models import PolymorphicModel
from django.dispatch import receiver


class CmsPost(PolymorphicModel):
  '''
  TODO:
  share post on save
  public/moderation part

  search and indexes

  comments
  '''

  author = models.ForeignKey('auth.User', verbose_name=_("Автор"))
  title = models.CharField(max_length=200, verbose_name=_("Название"))
  category = models.ForeignKey('CmsCategory', blank=True, null=False, verbose_name=_("Категория"))

  tags = TaggableManager(blank=True, verbose_name=_("Теги"))
  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"))
  published_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Дата публикации"))

  is_public = models.BooleanField(default=True, verbose_name=_("Опубликован"))
  is_moderated = models.BooleanField(default=True, verbose_name=_("Одобрен"))

  def _tags(self):
        return [t.name for t in self.tags.all()]

  def publish(self):
    '''
    TODO set is_public/is_moderated basing on category/etc
    '''
    self.published_date = timezone.now()

    self.save()

  @property
  def short_title(self):
    return truncatechars(self.title, 100)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = _("Пост")
    verbose_name_plural = _("Посты")
    permissions = (
        ("moderate_post", _("Модерация постов")),
        ("publish_post", _("Публикация постов")),
    )


class TextPost(CmsPost):
  text = RichTextUploadingField(verbose_name=_("Текст"))

  @property
  def short_text(self):
    return truncatechars(self.text, 400)

  class Meta:
    verbose_name = _("Текстовый пост")
    verbose_name_plural = _("Текстовые посты")
    permissions = (
        ("moderate_textpost", _("Модерация текстовых постов")),
    )

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})


class BinaryPost(CmsPost):
  file = models.ImageField(
    upload_to='uploads/%Y/%m/%d/',
    verbose_name=_("Файл"),
    null=True
  )
  description = models.TextField(max_length=200, verbose_name=_("Описание"))

  class Meta:
    verbose_name = _("Изображение")
    verbose_name_plural = _("Изображения")
    permissions = (
        ("moderate_binarypost", _("Модерация изображений")),
    )

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})


@receiver(models.signals.post_delete, sender=BinaryPost)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=BinaryPost)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = BinaryPost.objects.get(pk=instance.pk).file
    except BinaryPost.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)