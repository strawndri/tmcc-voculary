from django.urls import path
from . import views

urlpatterns = [
    path('gerar-textos', views.GeracaoTextoView, name='gerar-textos'),
    path('meus-textos', views.MeusTextosView, name='meus-textos'),
    path('obter-info-texto/<int:id_imagem>/', views.obter_info_texto, name='obter_info_texto'),
    path('alterar_nome/<int:texto_id>/', views.alterar_nome_texto, name='alterar_nome_texto'),
    path('desativar-texto/<int:texto_id>/', views.desativar_texto, name="desativar_texto"),
]