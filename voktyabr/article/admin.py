from django.contrib import admin
from django.db import models

from .models import Article

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FlatPageAdminRichText(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


admin.site.register(Article, FlatPageAdminRichText)

