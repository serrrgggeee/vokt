from django.conf.urls import url

from .import views


urlpatterns = [
    url(r'/(?P<id>\d+)/$', views.SinglePlaceView.as_view(), name='single_place'),

]