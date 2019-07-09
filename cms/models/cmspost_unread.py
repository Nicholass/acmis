from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q

from cms.models.cmspost import CmsPost
from django.contrib.auth.models import User

class CmsPostUnread(models.Model):
    user = models.ForeignKey('auth.User', verbose_name='Користувач')
    post = models.ForeignKey('cms.cmspost', verbose_name='Пост')

    @receiver(post_save, sender=CmsPost)
    def create_unread_record(sender, instance, created, **kwargs):
        if created:
            users = User.objects.filter(~Q(pk = instance.author.pk))
            for user in users:
                CmsPostUnread.objects.create(user=user, post=instance)