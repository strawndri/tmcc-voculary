from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views


urlpatterns = [

  # URLs padrões
  re_path(r'^cadastro/?$', views.cadastro_view, name='cadastro'),
  re_path(r'^login/?$', views.login_view, name='login'),
  re_path(r'^perfil/?$', views.perfil_view, name='perfil'),
  re_path(r'^logout/?$', views.logout_view, name='logout'),
    
  # Grupo de redefinição de senha
  path('redefinir-senha/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_html_email.html'), name="password_reset"),
  path('redefinir-senha/concluido/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
  path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('redefinir-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  
  # Reativação de conta
  path('reativar/<int:user_id>/<str:token>/', views.reativar_conta_view, name='reactivate_account'),
]