from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
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

    class Meta:
      verbose_name = _("Профиль")
      verbose_name_plural = _("Профили")
      permissions = (
          ("moderate_profile", _("Модерация профилей")),
      )