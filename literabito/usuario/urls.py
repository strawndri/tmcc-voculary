from django.urls import path
from . import views

urlpatterns = [
    path('apresentacao', views.cadastro, name='cadastro'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
]