# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-19 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20200419_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmsprofile',
            name='is_banned',
            field=models.BooleanField(default=False, verbose_name='Заблокувати користувача'),
        ),
    ]
