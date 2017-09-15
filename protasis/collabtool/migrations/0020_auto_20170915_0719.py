# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-15 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabtool', '0019_auto_20170915_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.ManyToManyField(null=True, to='collabtool.Code'),
        ),
        migrations.AlterField(
            model_name='project',
            name='data',
            field=models.ManyToManyField(null=True, to='collabtool.Data'),
        ),
        migrations.AlterField(
            model_name='project',
            name='group_access',
            field=models.ManyToManyField(null=True, to='collabtool.GroupAccess'),
        ),
        migrations.AlterField(
            model_name='project',
            name='institutions',
            field=models.ManyToManyField(null=True, to='collabtool.Institution'),
        ),
        migrations.AlterField(
            model_name='project',
            name='paper',
            field=models.ManyToManyField(null=True, to='collabtool.Paper'),
        ),
        migrations.AlterField(
            model_name='project',
            name='whitepaper',
            field=models.ManyToManyField(null=True, to='collabtool.WhitePaper'),
        ),
    ]