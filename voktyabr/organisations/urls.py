from django.conf.urls import url

from .import views


urlpatterns = [
    url(r'/(?P<slug>[\w-]+)/(?P<id>\d+)/$', views.OrganisationPageView.as_view(), name='organisations'),
    url(r'/(?P<slug>[\w-]+)/$', views.OrganisationView.as_view(), name='organisations'),


]


