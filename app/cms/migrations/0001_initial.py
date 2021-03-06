# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-28 22:10
from __future__ import unicode_literals

import ckeditor_uploader.fields
from cms.utils import PathAndRename
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import mptt.fields
import simplemde.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва')),
                ('route', models.CharField(max_length=200, verbose_name='Шлях')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='CmsPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('modifed_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата редагування')),
                ('is_permited', models.BooleanField(default=False, verbose_name='Зробити прихованим')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cms.CmsCategory', verbose_name='Категорія')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Пости',
                'permissions': (('moderate_cmspost', 'Модерація постів'), ('permited_access', 'Доступ до прихованих постів')),
            },
        ),
        migrations.CreateModel(
            name='CmsProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=PathAndRename('avatars/'), verbose_name='Аватар')),
                ('gender', models.CharField(blank=True, choices=[('BOY', 'Хлопець'), ('GIRL', 'Дівчина')], max_length=10, null=True, verbose_name='Стать')),
                ('birth_date', models.CharField(blank=True, max_length=80, null=True, verbose_name='Дата народження')),
                ('location', models.CharField(blank=True, max_length=80, null=True, verbose_name='Місце розташування')),
                ('facebook', models.CharField(blank=True, max_length=80, null=True, verbose_name='Facebook')),
                ('vk', models.CharField(blank=True, max_length=80, null=True, verbose_name='Vkontakte')),
                ('instagram', models.CharField(blank=True, max_length=80, null=True, verbose_name='Instagram')),
                ('twitter', models.CharField(blank=True, max_length=80, null=True, verbose_name='Twitter')),
                ('youtube', models.CharField(blank=True, max_length=80, null=True, verbose_name='YouTube')),
                ('telegram', models.CharField(blank=True, max_length=80, null=True, verbose_name='Telegram')),
                ('skype', models.CharField(blank=True, max_length=80, null=True, verbose_name='Skype')),
                ('last_activity', models.DateTimeField(blank=True, null=True, verbose_name='Був на сайті')),
                ('email_change_token', models.CharField(max_length=42, verbose_name='Код підтвердження зміни e-mail')),
                ('new_email', models.CharField(blank=True, max_length=256, null=True, verbose_name='Новий e-mail')),
                ('email_verefied', models.BooleanField(default=False, verbose_name='Підтвердити e-mail користувача')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профіль користувача',
                'verbose_name_plural': 'Профілі користувачів',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', simplemde.fields.SimpleMDEField(verbose_name='Текст')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Видалено')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, unique=True, verbose_name='Дата створення')),
                ('modifed_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата редагування')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='cms.Comment', verbose_name='Відповідь на')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.CmsPost', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
                'permissions': (('moderate_comment', 'Модерація коментарів'),),
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('file', models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='Файл')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='Опис')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('modifed_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата редагування')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Мапа',
                'verbose_name_plural': 'Мапи',
                'permissions': (('moderate_cmspost', 'Модерація мап'), ('map_access', 'Доступ до мап')),
            },
        ),
    ]
