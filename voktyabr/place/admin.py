from django.contrib import admin
from django.forms import ModelForm
from django_mptt_admin.admin import DjangoMpttAdmin
from django.db import models

from .models import Place, Photo

from suit_redactor.widgets import RedactorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CKEditorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


class PageForm(ModelForm):
    class Meta:
        pass


class PhotoAdmin(admin.StackedInline):
    model = Photo
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


class PlaceAdmin(DjangoMpttAdmin):
    form = PageForm

    class Meta:
        verbose_name_plural = 'place'
        app_label = 'места'
    tree_auto_open = 0
    list_display = ('name',)
    ordering = ('name',)
    inlines = [PhotoAdmin]

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }



admin.site.register(Place, PlaceAdmin)
admin.site.register(Photo)
