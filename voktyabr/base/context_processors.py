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
        'categories': Place.objects.all(),
        'BOOKS': Book.objects.all(),
        'ORGANISATIONS': Organisation.objects.filter(parent=None).order_by('order'),
        'ORGANISATION': Organisation.objects.filter(parent__slug=slug).order_by('order'),

    }