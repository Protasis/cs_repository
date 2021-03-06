# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0017_project_wiki'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='institutions',
            field=models.ManyToManyField(to='collabtool.Institution'),
        ),
        migrations.AlterField(
            model_name='project',
            name='wiki',
            field=models.URLField(default=b'/collabtool/wiki/'),
        ),
    ]
