from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),

    # Recuperação de senha
    path('senha/recuperar/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html',
        email_template_name='usuarios/password_reset_email.html',
        subject_template_name='usuarios/password_reset_subject.txt',
        success_url=reverse_lazy('usuarios:password_reset_done'),
    ), name='password_reset'),
    path('senha/recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html',
    ), name='password_reset_done'),
    path('senha/redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html',
        success_url=reverse_lazy('usuarios:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('senha/redefinir/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html',
    ), name='password_reset_complete'),
]
