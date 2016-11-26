from django.views.generic import TemplateView


class OrganisationView(TemplateView):
    template_name = 'organisation/menu_organisation.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     return context


class OrganisationPageView(TemplateView):
    template_name = 'organisation/page_organisation.html'


