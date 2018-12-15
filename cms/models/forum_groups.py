from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils.translation import ugettext as _

from pybb.models import Forum
from django.contrib.auth.models import Group

class ForumGroups(models.Model):
  forum = models.OneToOneField(Forum, on_delete=models.CASCADE, related_name='groups')

  groups = models.ManyToManyField(Group, blank=True, verbose_name=_("Groups with aditional access to forum"))

  @receiver(post_save, sender=Forum)
  def create_forum_groups(sender, instance, created, **kwargs):
    if created:
      ForumGroups.objects.create(forum=instance)

  @receiver(post_save, sender=Forum)
  def save_forum_groups(sender, instance, **kwargs):
    instance.groups.save()

  class Meta:
    verbose_name = _("Forum group")
    verbose_name_plural = _("Forum groups")
    permissions = (
      ("change_forumn_access", _("Change aditional access to forum")),
    )