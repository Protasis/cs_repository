# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0045_auto_20171004_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='data',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='project',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='report',
            name='group_access',
            field=models.ManyToManyField(blank=True, null=True, to='collabtool.GroupAccess'),
        ),
    ]
