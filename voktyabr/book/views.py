from django.views.generic import TemplateView
from .models import Book


class BooksView(TemplateView):
    template_name = 'book/books.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        return data


class BookView(TemplateView):
    template_name = 'book/book.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['pages'] = Book.objects.filter(parent_id=id, show=True).order_by('order')
        return data


class PageView(TemplateView):
    template_name = 'book/page.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['page'] = Book.objects.get(pk=id, show=True)
        return data

