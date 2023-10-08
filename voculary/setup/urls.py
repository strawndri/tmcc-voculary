# from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from usuario.admin import admin_site
from django.views.static import serve 


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', include('home.urls')),
    path('', include('usuario.urls')),
    path('', include('gerenciamento_texto.urls')),
    path('', include('ajuda.urls')),
    path('admin/', admin_site.urls),
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'setup.views.erro_404'