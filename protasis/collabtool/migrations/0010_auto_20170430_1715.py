# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 00:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0009_auto_20170430_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_code', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='data',
            field=models.FileField(blank=True, null=True, upload_to='data/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='data_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_data', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='paper',
            field=models.FileField(blank=True, null=True, upload_to='paper/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='paper_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_paper', to=settings.AUTH_USER_MODEL),
        ),
    ]