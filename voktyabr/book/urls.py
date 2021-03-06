from django.conf.urls import url

from .import views


urlpatterns = [
    url(r'ajax/(?P<id>\d+)/$', views.BookAjaxView.as_view(), name='book_ajax'),
    url(r'page/(?P<id>\d+)/$', views.PageView.as_view(), name='page'),
    url(r'(?P<id>\d+)/$', views.BookView.as_view(), name='book'),
    url(r'$', views.BooksView.as_view(), name='books'),


]