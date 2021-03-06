# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0054_auto_20171005_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverable',
            name='advisories',
            field=models.CharField(blank=True, help_text=b'List of advisory IDs separated by commas.', max_length=256),
        ),
        migrations.AddField(
            model_name='paper',
            name='advisories',
            field=models.CharField(blank=True, help_text=b'List of advisory IDs separated by commas.', max_length=256),
        ),
        migrations.AddField(
            model_name='report',
            name='advisories',
            field=models.CharField(blank=True, help_text=b'List of advisory IDs separated by commas.', max_length=256),
        ),
    ]
