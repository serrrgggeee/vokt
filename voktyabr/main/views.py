from django.views.generic import  TemplateView


class ListOktMainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(ListOktMainView, self).get_context_data(**kwargs)
        return context

