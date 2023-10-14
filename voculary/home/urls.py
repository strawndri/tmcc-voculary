from django.urls import path, re_path
from . import views

urlpatterns = [
    path('enviar_email/', views.enviar_email, name='enviar_email'),
    path('', views.home, name='home'),
    re_path(r'^home/?$', views.home, name='home'),
]