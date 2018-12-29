from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.utils.encoding import force_text
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group
from pybb.profiles import PybbProfile

class CmsProfile(PybbProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    birth_date = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Birth date"))
    location = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Location"))
    site = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Site"))

    facebook = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Facebook"))
    vk = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Vkontakte"))
    instagram = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Instagram"))
    twitter = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Twitter"))
    youtube = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("YouTube"))

    jabber = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Jabber"))
    telegram = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Telegram"))
    skype = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("Skype"))
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name=_("Last online"))

    hide_email = models.BooleanField(default=True, verbose_name=_("Hide e-mail"))

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return getattr(settings, 'STATIC_URL', '') + 'pybb/img/default_avatar.jpg'

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
        return reverse('another_profile', kwargs={'username': self.user.username})

    '''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CmsProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    '''

    class Meta:
      verbose_name = _("Profile")
      verbose_name_plural = _("Profiles")
      permissions = (
          ("moderate_cmsprofile", _("Moderate profiles")),
      )

    @receiver(post_save, sender=User)
    def add_to_default_group(sender, instance, created, **kwargs):
        if created and not instance.is_superuser:
            group = Group.objects.get(name=settings.DEFAULT_REGISTRATION_GROUP)
            instance.groups.add(group)