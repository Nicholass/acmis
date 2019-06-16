from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import force_text
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group
from cms.utils import PathAndRename

GENDER = (
    ('BOY', 'Хлопець'),
    ('GIRL', 'Дівчина'),
)

class CmsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(upload_to=PathAndRename('avatars/'), blank=True, null=True, verbose_name='Аватар')
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER, verbose_name='Стать')
    birth_date = models.CharField(max_length=80, null=True, blank=True, verbose_name='Дата народження')
    location = models.CharField(max_length=80, null=True, blank=True, verbose_name='Місце розташування')

    facebook = models.CharField(max_length=80, null=True, blank=True, verbose_name='Facebook')
    vk = models.CharField(max_length=80, null=True, blank=True, verbose_name='Vkontakte')
    instagram = models.CharField(max_length=80, null=True, blank=True, verbose_name='Instagram')
    twitter = models.CharField(max_length=80, null=True, blank=True, verbose_name='Twitter')
    youtube = models.CharField(max_length=80, null=True, blank=True, verbose_name='YouTube')

    telegram = models.CharField(max_length=80, null=True, blank=True, verbose_name='Telegram')
    skype = models.CharField(max_length=80, null=True, blank=True, verbose_name='Skype')
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name='Був на сайті')

    email_change_token = models.CharField(max_length=42, verbose_name='Код підтвердження зміни e-mail')
    new_email = models.CharField(max_length=256, verbose_name='Новий e-mail')

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return getattr(settings, 'AVATAR_DEFAULT', '')

    @property
    def online(self):
        if self.last_activity:
            now = timezone.now()
            if now < self.last_activity + timezone.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return True

        return False

    def get_display_name(self):
        try:
            if hasattr(self, 'user'):  # we have OneToOne foreign key to user model
                return self.user.get_username()
        except Exception:
            return force_text(self)

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.user.username})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CmsProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
      verbose_name = 'Профіль користувача'
      verbose_name_plural = 'Профілі користувачів'

    @receiver(post_save, sender=User)
    def add_to_default_group(sender, instance, created, **kwargs):
        if created and not instance.is_superuser:
            group = Group.objects.get(name=settings.DEFAULT_REGISTRATION_GROUP)
            instance.groups.add(group)