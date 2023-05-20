from django.urls import path
from . import views

urlpatterns = [
    path('minhas-pastas', views.minhas_pastas, name='minhas-pastas'),
]