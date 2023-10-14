from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    re_path(r'^cadastro/?$', views.CadastroView, name='cadastro'),
    re_path(r'^login/?$', views.LoginView, name='login'),
    re_path(r'^perfil/?$', views.PerfilView, name='perfil'),
    re_path(r'^logout/?$', views.LogoutView, name='logout'),
    
    # Grupo de redefinição de senha
    re_path(r'^redefinir-senha/?$', auth_views.PasswordResetView.as_view(), name="password_reset"),
    re_path(r'^redefinir-senha/concluido/?$', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    re_path(r'^redefinir-senha/<uidb64>/<token>/?$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^redefinir-senha/concluido/?$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    re_path(r'^reativar/<int:user_id>/<str:token>/?$', views.ReativarContaView, name='reactivate_account'),
]