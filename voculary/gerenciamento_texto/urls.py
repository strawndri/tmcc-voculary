from django.urls import path
from . import views

urlpatterns = [
    path('gerar-textos', views.GeracaoTextoView, name='gerar-textos'),
    path('meus-textos', views.MeusTextosView, name='meus-textos'),

]