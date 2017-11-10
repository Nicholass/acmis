from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager

class Post(models.Model):
  '''
  TODO:
  nice and transperent ENUM types for KIND and CATEGORY
  CATGORY should depend on TYPE
  should be easy to use in urls
  '''
  author = models.ForeignKey('auth.User')
  title = models.CharField(max_length=200)
  category = models.ForeignKey('Category', blank=True, null=False)

  text = models.TextField()
  tags = TaggableManager()
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True)

  def publish(self):
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
    self.kind = DATA_KINDS[self.name] #todo compute
    #TODO: validate here
    self.save()

  def __str__(self):
    return self.name
