# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-15 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0021_auto_20170915_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='group_access',
            field=models.ManyToManyField(blank=True, to='collabtool.GroupAccess'),
        ),
    ]
