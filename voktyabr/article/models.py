from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from meta.models import ModelMeta


class Article(ModelMeta, models.Model):
    CHOICES = (
        ('new', 'Новости'),
        ('act', 'Мероприятия'),
        ('nat', 'Природа'),
    )

    name = models.CharField('Название статьи',  max_length=128, default='')
    image = models.ImageField(upload_to='article',
                              verbose_name='Article', null=True, blank=True)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    pub_date = models.DateTimeField('Дата размещения',default=now)
    comment = models.TextField(verbose_name='коментарии к фотографии', null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    category = models.CharField('тип статьи', max_length=3, choices=CHOICES, null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    seo_title = models.CharField(max_length=160, null=True, blank=True)
    seo_description = models.CharField(max_length=160, null=True, blank=True)

    def __str__(self):
        return self.name or self.code or ''

    _metadata = {
        # в шаблоне если use_title_tag возвращает True, то генерируется title
        'use_title_tag': 'seo_title',
        'title': 'seo_title',
        'description': 'seo_description',
    }


