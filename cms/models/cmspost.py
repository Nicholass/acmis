from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.template.defaultfilters import truncatechars
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from cms.models.comment import Comment

class CmsPost(models.Model):
    author = models.ForeignKey('auth.User', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    category = models.ForeignKey('CmsCategory', blank=True, null=False, verbose_name='Категорія')

    text = RichTextUploadingField(verbose_name='Текст')

    tags = TaggableManager(blank=True, verbose_name='Тэги')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата створення')
    modifed_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата редагування')
    is_permited = models.BooleanField(default=False, verbose_name='Зробити прихованим')

    last_comment = models.ForeignKey('Comment', verbose_name='Останній коментар', blank=True, null=True)

    @property
    def short_title(self):
        return truncatechars(self.title, 100)

    def _tags(self):
        return [t.name for t in self.tags.all()]

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    @receiver(post_save, sender=Comment)
    def change_last_comment_on_create(sender, instance, created, **kwargs):
        post = CmsPost.objects.get(pk=instance.post.pk)

        if created:
            post.last_comment = instance
        else:
            if instance.is_deleted:
                post.last_comment = Comment.objects.filter(post=instance.post, is_deleted=False).order_by('-created_date').first()

        post.save()

    @receiver(pre_delete, sender=Comment)
    def change_last_comment_on_delete(sender, instance, **kwargs):
        post = CmsPost.objects.get(pk=instance.post.pk)
        post.last_comment = Comment.objects.filter(post=instance.post, is_deleted=False).order_by('-created_date').first()
        post.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        permissions = (
            ('moderate_cmspost', 'Модерація постів'),
            ('permited_access', 'Доступ до прихованих постів'),
        )
