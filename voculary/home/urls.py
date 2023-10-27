from django.urls import path, re_path

from . import views

urlpatterns = [

    # URLs relacionadas à página principal
    path('', views.home_view, name='home'),
    re_path(r'^home/?$', views.home_view, name='home'),

    # URL de reativação de conta
    path('enviar_email/', views.enviar_email_reativacao_view, name='enviar_email'),
]