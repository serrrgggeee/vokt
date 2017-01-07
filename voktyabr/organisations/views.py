from django.views.generic import TemplateView

from .models import Organisation


class OrganisationView(TemplateView):
    template_name = 'organisation/organisation.html'

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug', '')
        try:
            organisation = Organisation.objects.get(slug=slug, show=True)
        except Organisation.DoesNotExist:
            organisation = ''
        context = super().get_context_data(**kwargs)
        context['organisation'] = organisation
        return context


class OrganisationPageView(TemplateView):
    template_name = 'organisation/page_organisation.html'

    def get_context_data(self, **kwargs):
        id = kwargs.get('id', '')
        try:
            organisation = Organisation.objects.get(id=id, show=True)
        except Organisation.DoesNotExist:
            organisation = ''
        context = super().get_context_data(**kwargs)
        context['page'] = organisation
        return context