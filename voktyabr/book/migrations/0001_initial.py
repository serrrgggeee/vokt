# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 12:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название книги')),
                ('type_book', models.CharField(blank=True, max_length=128, null=True, verbose_name='Тип книги')),
                ('show', models.BooleanField(default=False, verbose_name='Отображать на сайте')),
                ('order', models.IntegerField(verbose_name='номер цтраницы')),
                ('description', models.TextField(verbose_name='Описание')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Срок размещения в днях')),
                ('image_book', models.ImageField(blank=True, null=True, upload_to='book', verbose_name='image_book')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='book.Book')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
