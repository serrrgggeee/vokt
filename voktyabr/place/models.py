from django.db import models
from datetime import datetime
from django.utils.timezone import now

from mptt.models import MPTTModel, TreeForeignKey
from redactor.fields import RedactorField
from tinymce.models import HTMLField
#from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

class Place(MPTTModel):
    name = models.CharField('Название населенного пункта',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_place = models.CharField('Тип населенного пункта',  max_length=128)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    first_order = models.BooleanField(default=False,  verbose_name='Первые в списке')
    description = models.TextField(verbose_name='Описание')
    #description = RichTextField()
    #description = HTMLField(verbose_name='Описание')
    pub_date = models.DateTimeField('Срок размещения в днях',default=now)
    image_description = models.ImageField(upload_to='media/description',
                              verbose_name='Image', blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name or self.code or ''

class Photo(models.Model):
    name = models.CharField('Название фотографии',  max_length=128, default='')
    image = models.ImageField(upload_to='media/main_page',
                              verbose_name='Image', default='')
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    pub_date = models.DateTimeField('Дата размещения',default=now)
    description = models.TextField(verbose_name='Описание', default='')
    comment = models.TextField(verbose_name='коментарии к фотографии', null=True, blank=True,)
    user = models.ForeignKey(User, blank=True, null=True)
    photo = models.ForeignKey(Place, related_name="photo", verbose_name='Местро расположения')