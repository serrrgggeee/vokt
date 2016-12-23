from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

from meta.models import ModelMeta

from article.models import Article


class Place(MPTTModel, ModelMeta):
    name = models.CharField('Название населенного пункта',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_place = models.CharField('Тип населенного пункта',  max_length=128)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    first_order = models.BooleanField(default=False,  verbose_name='Первые в списке')
    pub_date = models.DateTimeField('Срок размещения в днях', default=now)
    image_description = models.ImageField(upload_to='main_page', verbose_name='Image', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    seo_title = models.CharField(max_length=160, null=True, blank=True)
    seo_description = models.CharField(max_length=160, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name or self.code or ''

    _metadata = {
        # в шаблоне если use_title_tag возвращает True, то генерируется title
        'use_title_tag': 'seo_title',
        'title': 'seo_title',
        'description': 'seo_description',
    }


class Photo(models.Model):
    name = models.CharField('Название фотографии',  max_length=128, default='')
    image = models.ImageField(upload_to='description',
                              verbose_name='Image', default='')
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    pub_date = models.DateTimeField('Дата размещения',default=now)
    description = models.TextField(verbose_name='Описание', default='')
    comment = models.TextField(verbose_name='коментарии к фотографии', null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    photo = models.ForeignKey(Place, related_name="photo", verbose_name='Местро расположения')
    article = models.ForeignKey(Article, related_name="article", verbose_name='Привязанная статья', null=True, blank=True)


