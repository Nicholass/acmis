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
from sorl.thumbnail import ImageField


class CmsPost(PolymorphicModel):
  '''
  TODO:
  share post on save
  public/moderation part

  search and indexes

  comments
  '''

  author = models.ForeignKey('auth.User', verbose_name=_("Author"))
  title = models.CharField(max_length=200, verbose_name=_("Title"))
  category = models.ForeignKey('CmsCategory', blank=True, null=False, verbose_name=_("Category"))

  tags = TaggableManager(blank=True, verbose_name=_("Tags"))
  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Creation date"))

  is_public = models.BooleanField(default=True, verbose_name=_("Published"), help_text=_("If not сhecked, the post will be saved as a draft"))
  is_moderated = models.BooleanField(default=True, verbose_name=_("Approved"), help_text=_("If not сhecked, then the post will not be displayed"))

  def _tags(self):
        return [t.name for t in self.tags.all()]

  @property
  def short_title(self):
    return truncatechars(self.title, 100)

  def get_absolute_url(self):
    return "/post/%i/" % self.pk

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = _("Post")
    verbose_name_plural = _("Posts")
    permissions = (
        ("moderate_cmspost", _("Moderate posts")),
        ("publish_cmspost", _("Publish posts")),
    )


class TextPost(CmsPost):
  text = RichTextUploadingField(verbose_name=_("Text"))

  @property
  def short_text(self):
    return truncatechars(self.text, 400)

  class Meta:
    verbose_name = _("Text post")
    verbose_name_plural = _("Text posts")
    permissions = (
        ("moderate_textpost", _("Moderate text post")),
    )

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})


class BinaryPost(CmsPost):
  file = ImageField(
    upload_to='uploads/%Y/%m/%d/',
    verbose_name=_("File"),
    null=True
  )
  description = models.TextField(max_length=200, verbose_name=_("Description"), blank=True)

  class Meta:
    verbose_name = _("Image post")
    verbose_name_plural = _("Images posts")
    permissions = (
        ("moderate_binarypost", _("Moderate images posts")),
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