# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-15 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0022_auto_20170915_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='slug',
            field=models.SlugField(default=b'', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='code',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='data',
            name='slug',
            field=models.SlugField(default=b'', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='data',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]