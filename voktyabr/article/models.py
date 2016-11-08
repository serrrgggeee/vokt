from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Article(models.Model):
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
    description = models.TextField(verbose_name='Описание', default='')
    comment = models.TextField(verbose_name='коментарии к фотографии', null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    category = models.CharField('тип статьи', max_length=3, choices=CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name or self.code or ''


