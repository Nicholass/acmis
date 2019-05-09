from django.db import models
from django.template.defaultfilters import truncatechars
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.utils.translation import ugettext as _


class Comment(MPTTModel):

  post = models.ForeignKey('CmsPost', on_delete=models.CASCADE, verbose_name=_("Post"))
  author = models.ForeignKey('auth.User', verbose_name=_("Author"))
  text = models.TextField(max_length=600, verbose_name=_("Text"))

  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name=_("Reply to"))

  is_moderated = models.BooleanField(default=True, verbose_name=_("Approved"), help_text=_("If not сhecked, then the comment will not be displayed"))
  is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

  created_date = models.DateTimeField(default=timezone.now, verbose_name=_("Date created"), unique=True)
  modifed_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Dete edited"))

  @property
  def short_text(self):
    return truncatechars(self.text, 50)

  def __str__(self):
    return self.text

  class Meta:
    verbose_name = _("Comment")
    verbose_name_plural = _("Comments")
    permissions = (
        ("moderate_comment", _("Moderate comments")),
    )

  class MPTTMeta:
    order_insertion_by = ['created_date']
