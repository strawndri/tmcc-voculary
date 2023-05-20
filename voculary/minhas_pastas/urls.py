from django.urls import path
from . import views

urlpatterns = [
    path('minhas_pastas', views.minhas_pastas, name='minhas_pastas'),
]