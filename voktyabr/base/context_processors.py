from django.conf import settings
from place.models import Place
from book.models import Book


class Menu():
    def _get_menu(self):
        return Place.objects.all()


def common(request):
    return {
        'DEBUG': settings.DEBUG,
        'categories': Place.objects.all(),
        'BOOKS': Book.objects.all(),
    }