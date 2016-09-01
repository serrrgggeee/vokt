from django.contrib import admin
from django.db import models
from django.forms import ModelForm

from .models import Place

#from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_mptt_admin.admin import DjangoMpttAdmin
from redactor.widgets import RedactorEditor
from suit_redactor.widgets import RedactorWidget

class PageForm(ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'en'})
        }

class PlaceAdmin(DjangoMpttAdmin):
    form = PageForm
    class Meta:
        verbose_name_plural = 'place'
        app_label = 'места'
    tree_auto_open = 0
    list_display = ('name',)
    ordering = ('name',)

    # formfield_overrides = {
    #     models.TextField: {'widget': AdminRedactorEditor}
    # }

admin.site.register(Place, PlaceAdmin)