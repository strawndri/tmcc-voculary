from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.CadastroView, name='cadastro'),
    path('login/', views.LoginView, name='login'),
    path('perfil/', views.PerfilView, name='perfil'),
    path('logout/', views.LogoutView, name='logout'),
    
    # Grupo de redefinição de senha
    path('redefinir-senha/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('redefinir-senha/concluido/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('redefinir-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('reativar/<int:user_id>/<str:token>/', views.ReativarContaView, name='reactivate_account'),
]