from django.shortcuts import render

from django.views.generic import View, TemplateView
from .models import Place, Photo

class SinglePlaceView(TemplateView):
    template_name = 'place/single_place.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['single_place']=Place.objects.prefetch_related('photo').get(id=id)
        return data