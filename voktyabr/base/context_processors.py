from django.conf import settings
from place.models import Place
from book.models import Book
from organisations.models import Organisation


class Menu():
    def _get_menu(self):
        return Place.objects.all()


def common(request, **kwargs):
    try:
        slug = request.path.split('/')[2]
    except IndexError:
        slug = ''
        print('list index out of range')
    return {
        'DEBUG': settings.DEBUG,
        'categories': Place.objects.filter(show=True),
        'BOOKS': Book.objects.filter(show=True),
        'ORGANISATIONS': Organisation.objects.filter(show=True, parent=None).order_by('order'),
        'ORGANISATION': Organisation.objects.filter(show=True, parent__slug=slug).order_by('order'),

    }