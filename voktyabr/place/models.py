from django.db import models
from datetime import datetime


from mptt.models import MPTTModel, TreeForeignKey
from redactor.fields import RedactorField
from tinymce.models import HTMLField
#from ckeditor.fields import RichTextField

class Place(MPTTModel):
    name = models.CharField('Название населенного пункта',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_place = models.CharField('Тип населенного пункта',  max_length=128)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    first_order = models.BooleanField(default=False,  verbose_name='Первые в списке')
    description = models.TextField(verbose_name='Описание')
    #description = RichTextField()
    #description = HTMLField(verbose_name='Описание')
    pub_date = models.DateTimeField('Срок размещения в днях',default=datetime.now() )
    image_description = models.ImageField(upload_to='/description',
                              verbose_name='Image', blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name or self.code or ''

class Photo(models.Model):
    image = models.ImageField(upload_to='media',
                              verbose_name='Image', blank=True, null=True)
    photo = models.ForeignKey(Place, related_name="photo", verbose_name='Группа')