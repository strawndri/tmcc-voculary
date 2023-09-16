from django.urls import path
from . import views

urlpatterns = [
    path('gerar-textos', views.GeracaoTextoView, name='gerar-textos'),
    path('meus-textos', views.MeusTextosView, name='meus-textos'),
    path('obter-info-texto/<int:id_imagem>/', views.obter_info_texto, name='obter_info_texto'),
]