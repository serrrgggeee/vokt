# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 10:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
        ('place', '0004_auto_20161014_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='article.Article', verbose_name='Привязанная статья'),
        ),
    ]
