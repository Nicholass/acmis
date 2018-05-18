from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

class EmailChange(models.Model):
  auth_key = models.CharField(max_length=42, verbose_name=_("Код подтверждения"))
  user = models.ForeignKey(User, verbose_name=_("Пользователь"))
  new_email = models.CharField(max_length=256, verbose_name=_("Новый email"))