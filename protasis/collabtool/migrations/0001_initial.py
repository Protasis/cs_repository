# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 09:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('surname', models.CharField(max_length=256)),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutions', to='collabtool.Author')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collabtool.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
                ('abstract', models.TextField()),
                ('code', models.URLField()),
                ('data', models.URLField()),
                ('paper', models.URLField()),
                ('url', models.URLField()),
                ('bibtex', models.TextField()),
                ('authors', models.ManyToManyField(to='collabtool.InstitutionAuthor')),
                ('corresponding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='collabtool.InstitutionAuthor')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('acronym', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collabtool.Venue'),
        ),
    ]
