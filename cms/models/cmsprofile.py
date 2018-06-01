from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from django.contrib.auth.models import User, Group

TZ_CHOICES = [(float(x[0]), x[1]) for x in (
    (-12, '-12'), (-11, '-11'), (-10, '-10'), (-9.5, '-09.5'), (-9, '-09'),
    (-8.5, '-08.5'), (-8, '-08 PST'), (-7, '-07 MST'), (-6, '-06 CST'),
    (-5, '-05 EST'), (-4, '-04 AST'), (-3.5, '-03.5'), (-3, '-03 ADT'),
    (-2, '-02'), (-1, '-01'), (0, '00 GMT'), (1, '+01 CET'), (2, '+02'),
    (3, '+03'), (3.5, '+03.5'), (4, '+04'), (4.5, '+04.5'), (5, '+05'),
    (5.5, '+05.5'), (6, '+06'), (6.5, '+06.5'), (7, '+07'), (8, '+08'),
    (9, '+09'), (9.5, '+09.5'), (10, '+10'), (10.5, '+10.5'), (11, '+11'),
    (11.5, '+11.5'), (12, '+12'), (13, '+13'), (14, '+14'),
)]

class CmsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    signature = models.TextField(_('Подпись'), blank=True, max_length=1024)
    signature_html = models.TextField(_('HTML подпись'), blank=True, max_length=1054)
    time_zone = models.FloatField(_('Часовой пояс'), choices=TZ_CHOICES, default=float(2))
    language = models.CharField(_('Язык'), max_length=10, blank=True, choices=settings.LANGUAGES,
                                default=get_supported_language_variant(settings.LANGUAGE_CODE, strict=True))
    show_signatures = models.BooleanField(_('Показывать подпись'), default=True)
    post_count = models.IntegerField(_('Колличество постов'), blank=True, default=0)
    autosubscribe = models.BooleanField(_('Автоматическая подписка'),
                                        help_text=_('Автоматическая подписка на темы в которые вы отвечаете'),
                                        default=False)

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

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return getattr(settings, 'STATIC_URL', '') + 'pybb/img/default_avatar.jpg'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CmsProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
      verbose_name = _("Профиль")
      verbose_name_plural = _("Профили")
      permissions = (
          ("moderate_profile", _("Модерация профилей")),
      )

    @receiver(post_save, sender=User)
    def add_to_default_group(sender, instance, created, **kwargs):
        if created and not instance.is_superuser:
            group = Group.objects.get(name=settings.DEFAULT_REGISTRATION_GROUP)
            instance.groups.add(group)