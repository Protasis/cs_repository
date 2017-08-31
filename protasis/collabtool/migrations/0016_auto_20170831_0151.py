# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('collabtool', '0015_auto_20170830_0535'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('write', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='code_access',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='data',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='data_access',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='paper_access',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='project_access',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userperms',
            name='whitepaper_access',
        ),
        migrations.AddField(
            model_name='code',
            name='code',
            field=models.FileField(blank=True, null=True, upload_to=b'paper/'),
        ),
        migrations.AddField(
            model_name='data',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='UserPerms',
        ),
        migrations.AddField(
            model_name='code',
            name='group_access',
            field=models.ManyToManyField(to='collabtool.GroupAccess'),
        ),
        migrations.AddField(
            model_name='data',
            name='group_access',
            field=models.ManyToManyField(to='collabtool.GroupAccess'),
        ),
        migrations.AddField(
            model_name='paper',
            name='group_access',
            field=models.ManyToManyField(to='collabtool.GroupAccess'),
        ),
        migrations.AddField(
            model_name='project',
            name='group_access',
            field=models.ManyToManyField(to='collabtool.GroupAccess'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='group_access',
            field=models.ManyToManyField(to='collabtool.GroupAccess'),
        ),
    ]
