from django.db import models
from django.conf import settings


class PunbbUser(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(PunbbGroup, verbose_name='group')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=150)
    title = models.CharField(max_length=150, blank=True)
    realname = models.CharField(max_length=120, blank=True)
    url = models.CharField(max_length=255, blank=True)
    jabber = models.CharField(max_length=225, blank=True)
    icq = models.CharField(max_length=36, blank=True)
    msn = models.CharField(max_length=150, blank=True)
    aim = models.CharField(max_length=90, blank=True)
    yahoo = models.CharField(max_length=90, blank=True)
    location = models.CharField(max_length=90, blank=True)
    use_avatar = models.BooleanField()
    signature = models.TextField(blank=True)
    disp_topics = models.IntegerField(null=True, blank=True)
    disp_posts = models.IntegerField(null=True, blank=True)
    email_setting = models.BooleanField()
    save_pass = models.BooleanField()
    notify_with_post = models.BooleanField()
    show_smilies = models.BooleanField()
    show_img = models.BooleanField()
    show_img_sig = models.BooleanField()
    show_avatars = models.BooleanField()
    show_sig = models.BooleanField()
    timezone = models.FloatField()
    language = models.CharField(max_length=75)
    style = models.CharField(max_length=75)
    num_posts = models.IntegerField()
    last_post = models.IntegerField(null=True, blank=True)
    registered = models.IntegerField()
    registration_ip = models.CharField(max_length=45)
    last_visit = models.IntegerField()
    admin_note = models.CharField(max_length=90, blank=True)
    activate_string = models.CharField(max_length=150, blank=True)
    activate_key = models.CharField(max_length=24, blank=True)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = u'%susers' % settings.PUNBB_TABLES_PREFIX
        verbose_name = 'PunBB user'
