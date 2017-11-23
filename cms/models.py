from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from taggit.managers import TaggableManager

class Post(models.Model):
  '''
  TODO:
  share post on save
  public/moderation part

  search and indexes

  comments
  '''
  author = models.ForeignKey('auth.User')
  title = models.CharField(max_length=200)
  category = models.ForeignKey('Category', blank=True, null=False)

  tags = TaggableManager()
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True)

  is_public = models.BooleanField(default=True)
  is_moderated = models.BooleanField(default=True)

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

class Category(models.Model):
  FILE = 0
  POST = 1
  UNKNOWN = 3
  KINDS = (
    (FILE, "File"),
    (POST, "Post"),
    (UNKNOWN, "Unknown"),
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
  )
  name = models.CharField(max_length=200)
  route = models.CharField(max_length=200)

  def publish(self):
    self.kind = DATA_KINDS[self.name]
    #TODO: validate here
    self.save()

  def __str__(self):
    return self.name

class TextPodst(Post):
  text = models.TextField()

class BinaryPost(Post):
  content = models.ImageField(blank=True, null=True) #TODO upload_to
