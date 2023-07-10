from django.urls import path
from . import views

urlpatterns = [
    path('', views.apresentacao, name='apresentacao'),
    path('apresentacao', views.apresentacao, name='apresentacao')
]