from django.contrib import admin
from django.forms import ModelForm
from django_mptt_admin.admin import DjangoMpttAdmin
from django.db import models

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Organisation


class OrganisationAdmin(DjangoMpttAdmin):

    class Meta:
        verbose_name_plural = 'организация'
        app_label = 'организации'
    tree_auto_open = 0
    list_display = ('name',)
    ordering = ('name',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


admin.site.register(Organisation, OrganisationAdmin)