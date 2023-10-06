# from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from usuario.admin import admin_site

urlpatterns = [
    path('', include('home.urls')),
    path('', include('usuario.urls')),
    path('', include('gerenciamento_texto.urls')),
    path('', include('ajuda.urls')),
    path('admin/', admin_site.urls),
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
