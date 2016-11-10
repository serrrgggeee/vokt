from django.views.generic import TemplateView
from .models import Place


class SinglePlaceView(TemplateView):
    template_name = 'place/book.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['single_place']=Place.objects.prefetch_related('photo').get(id=id)
        return data