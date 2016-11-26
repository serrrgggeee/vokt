from django.contrib import admin
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),


    url(r'^article', include('article.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^book', include('book.urls')),
    url(r'^organisation', include('organisations.urls')),
    url(r'^', include('place.urls')),
    url(r'^$', include('main.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()