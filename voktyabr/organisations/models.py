from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey


class Organisation(MPTTModel):
    slug = models.CharField('Slug организации',  max_length=128, unique=True, null=True, blank=True,)
    name = models.CharField('Название организации',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_organisation = models.CharField('Тип организации',  max_length=128, blank=True, null=True)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    order = models.IntegerField(verbose_name='порядок в списке', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField('Срок размещения в днях', default=now)
    image_organisation = models.ImageField(upload_to='organisation', verbose_name='image_organisation', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name