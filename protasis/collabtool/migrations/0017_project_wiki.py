# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0016_auto_20170831_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='wiki',
            field=models.URLField(default=b'wiki'),
        ),
    ]
