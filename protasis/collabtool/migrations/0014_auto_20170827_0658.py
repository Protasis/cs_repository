# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-27 13:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collabtool', '0013_data_project_whitepaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserPerms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usr_code_access', models.ManyToManyField(blank=True, related_name='can_access_paper', to='collabtool.Code')),
                ('usr_data_access', models.ManyToManyField(blank=True, related_name='can_access_paper', to='collabtool.Data')),
            ],
        ),
        migrations.RenameField(
            model_name='paper',
            old_name='code_access',
            new_name='pa_code_access',
        ),
        migrations.RenameField(
            model_name='paper',
            old_name='data_access',
            new_name='pa_data_access',
        ),
        migrations.RenameField(
            model_name='paper',
            old_name='paper_access',
            new_name='pa_paper_access',
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='abstract',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='authors',
            field=models.ManyToManyField(to='collabtool.InstitutionAuthor'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='bibtex',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='code',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='corresponding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='collabtool.InstitutionAuthor'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='data',
            field=models.FileField(blank=True, null=True, upload_to=b'data/'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='data_protected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='paper',
            field=models.FileField(blank=True, null=True, upload_to=b'paper/'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='slug',
            field=models.SlugField(default=b'', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='venue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collabtool.Venue'),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='wp_code_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_code_wp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='wp_data_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_data_wp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='wp_paper_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_paper_wp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userperms',
            name='usr_paper_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_paper', to='collabtool.Paper'),
        ),
        migrations.AddField(
            model_name='userperms',
            name='usr_project_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_paper', to='collabtool.Project'),
        ),
        migrations.AddField(
            model_name='userperms',
            name='usr_whitepaper_access',
            field=models.ManyToManyField(blank=True, related_name='can_access_paper', to='collabtool.WhitePaper'),
        ),
    ]
