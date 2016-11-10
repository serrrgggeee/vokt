from django.contrib import admin
from django.forms import ModelForm
from django_mptt_admin.admin import DjangoMpttAdmin
from django.db import models

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Book


class BookAdmin(DjangoMpttAdmin):

    class Meta:
        verbose_name_plural = 'книга'
        app_label = 'книги'
    tree_auto_open = 0
    list_display = ('name',)
    ordering = ('name',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


admin.site.register(Book, BookAdmin)