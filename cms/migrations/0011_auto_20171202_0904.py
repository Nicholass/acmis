# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-02 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='has_avatar',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]
