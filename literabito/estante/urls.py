from django.urls import path
from . import views

urlpatterns = [
    path('estante', views.estante, name='estante'),
]