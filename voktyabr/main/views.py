from django.shortcuts import render
from django.views.generic import View, TemplateView
from place.models import Place

class Menu():
    def _get_menu(self):
        return Place.objects.all()

class ListOktMainView(TemplateView, Menu):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(ListOktMainView, self).get_context_data(**kwargs)
        context['categories'] = self._get_menu()
        cat= self._get_menu()
        for c in cat:
            print(c.image_description.url)
        return context
