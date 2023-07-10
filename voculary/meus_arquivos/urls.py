from django.urls import path
from . import views

urlpatterns = [
    path('meus-arquivos', views.meus_arquivos, name='meus-arquivos'),
]