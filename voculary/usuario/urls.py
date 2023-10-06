from django.urls import path
from . import views
from . import admin

urlpatterns = [
    path('cadastro', views.CadastroView, name='cadastro'),
    path('login', views.LoginView, name='login'),
    path('perfil', views.PerfilView, name='perfil'),
    path('logout', views.LogoutView, name='logout'),
]

