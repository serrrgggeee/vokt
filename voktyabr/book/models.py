from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey


class Book(MPTTModel):
    name = models.CharField('Название книги',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_book = models.CharField('Тип книги',  max_length=128, blank=True, null=True)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    order = models.IntegerField(verbose_name='номер цтраницы')
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField('Срок размещения в днях', default=now)
    image_book = models.ImageField(upload_to='organisation', verbose_name='image_book', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    seo_title = models.CharField(max_length=160, null=True, blank=True)
    seo_description = models.CharField(max_length=160, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.name


