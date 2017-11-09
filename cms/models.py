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
  UNKNOWN = 'u'

  POST = 'p'
  FILE = 'f'
  KINDS = (
    (FILE, u'File'),
    (POST, u'Post'),
    (UNKNOWN, u'Unknown')
  )
  kind = models.CharField(
    max_length=254,
    null=False,
    blank=False,
    choices=KINDS,
    default=UNKNOWN,
  )


  MAP = 'm'
  PHOTO = 'p'
  CATEGORIES =(
    (MAP, u'Map'),
    (PHOTO, u'Photo'),
    (UNKNOWN, u'Unknown')
  )
  category = models.CharField(
    max_length=254,
    null=False,
    blank=False,
    choices=CATEGORIES,
    default=UNKNOWN,
  )

  author = models.ForeignKey('auth.User')
  title = models.CharField(max_length=200)


  text = models.TextField()
  tags = TaggableManager()
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True)

  def get_kind_verbose(self):
    return dict(Post.KINDS)[self.kind]

  def get_category_verbose(self):
    return dict(Post.CATEGORIES)[self.kind]

  def set_category_verbose(self, val):
    #TODO validation kind vs cat here
    self.kind = dict(Post.CATEGORIES)[val][0]


  def publish(self):
    self.published_date = timezone.now()
    self.kind = 'f' #todo compute
    #TODO: validate here
    self.save()

  def __str__(self):
    return self.title
