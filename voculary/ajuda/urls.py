from django.urls import path
from . import views

urlpatterns = [
    path('ajuda', views.ajuda, name='ajuda')
]