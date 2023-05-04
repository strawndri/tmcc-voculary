from django.urls import path
from . import views

urlpatterns = [
    path('apresentacao', views.apresentacao, name='apresentacao'),
]