from django.urls import path
from . import views

urlpatterns = [
    path('gerar-textos', views.geracao_texto_view, name='gerar-textos'),
    path('meus-textos', views.meus_textos_view, name='meus-textos'),
    path('obter-info-texto/<int:id_imagem>/', views.obter_info_texto_view, name='obter_info_texto'),
    path('alterar_nome/<int:id_imagem>/', views.alterar_nome_texto_view, name='alterar_nome_texto'),
    path('desativar-texto/<int:id_imagem>/', views.desativar_texto_view, name="desativar_texto"),
]