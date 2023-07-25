from django.urls import path
from . import views

urlpatterns = [
    path('reconhecimento_texto', views.reconhecimento_texto, name='reconhecimento_texto'),
]