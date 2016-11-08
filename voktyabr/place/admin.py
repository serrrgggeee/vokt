from django.contrib import admin
from django.forms import ModelForm
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Place, Photo

from suit_redactor.widgets import RedactorWidget


class PageForm(ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'en'})
        }


class PhotoAdmin(admin.StackedInline):
    model = Photo
    extra = 0


class PlaceAdmin(DjangoMpttAdmin):
    form = PageForm
    class Meta:
        verbose_name_plural = 'place'
        app_label = 'места'
    tree_auto_open = 0
    list_display = ('name',)
    ordering = ('name',)

    inlines = [PhotoAdmin]

    # formfield_overrides = {
    #     models.TextField: {'widget': AdminRedactorEditor}
    # }    

admin.site.register(Place, PlaceAdmin)
admin.site.register(Photo)
