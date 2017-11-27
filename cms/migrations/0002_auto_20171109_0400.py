# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-09 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('m', 'Map'), ('p', 'Photo'), ('u', 'Unknown')], default='u', max_length=254),
        ),
        migrations.AddField(
            model_name='post',
            name='kind',
            field=models.CharField(choices=[('f', 'File'), ('p', 'Post'), ('u', 'Unknown')], default='u', max_length=254),
        ),
    ]
