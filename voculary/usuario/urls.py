from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import admin

urlpatterns = [
    path('cadastro', views.CadastroView, name='cadastro'),
    path('login', views.LoginView, name='login'),
    path('perfil', views.PerfilView, name='perfil'),
    path('logout', views.LogoutView, name='logout'),
    path('redefinir-senha/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('redefinir-senha/concluido/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('redefinir/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reativar/<int:user_id>/<str:token>/', views.reativar_conta, name='reactivate_account'),
]

