from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from taggit.managers import TaggableManager

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatechars

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

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

class TextPost(Post):
  text = models.TextField(verbose_name=_("Текст"))

  class Meta:
    verbose_name = _("Текстовый пост")
    verbose_name_plural = _("Текстовые посты")

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})

class BinaryPost(Post):
  file = models.ImageField(
    blank=True,
    null=True,
    upload_to='uploads/%Y/%m/%d/',
    verbose_name=_("Файл")
  )
  description = models.TextField(max_length=200, verbose_name=_("Описание"))

  class Meta:
    verbose_name = _("Изображение")
    verbose_name_plural = _("Изображения")

  def get_absolute_url(self):
      return reverse('post_detail', kwargs={'pk': self.pk})

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
    'Drawing': FILE,
    'Map': FILE,
    'News': POST,
    'Photo': FILE,
    'Prose': POST,
    'Report': POST
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

  class MPTTMeta:
    order_insertion_by = ['created_date']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    has_avatar = models.BooleanField(default=False)
    birth_date = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Дата рождения"))
    location = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Местонахождение"))
    site = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Вебсайт"))

    facebook = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Facebook"))
    vk = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Vkontakte"))
    instagram = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Instagram"))
    twitter = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Twitter"))
    youtube = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("YouTube"))

    jabber = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Jabber"))
    telegram = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Telegram"))
    skype = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Skype"))

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
