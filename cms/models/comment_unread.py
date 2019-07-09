from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q

from cms.models.comment import Comment
from django.contrib.auth.models import User

class CommentUnread(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Користувач')
    post = models.ForeignKey('cms.cmspost', on_delete=models.CASCADE, verbose_name='Пост')
    comment = models.ForeignKey('cms.comment', on_delete=models.CASCADE, verbose_name='Коментар')

    @receiver(post_save, sender=Comment)
    def create_unread_record(sender, instance, created, **kwargs):
        if created:
            users = User.objects.filter(~Q(pk = instance.author.pk))
            for user in users:
                CommentUnread.objects.create(user=user, post=instance.post, comment=instance)