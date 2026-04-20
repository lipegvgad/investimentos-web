from django.urls import path, reverse_lazy
from . import views

app_name = 'aportes'

urlpatterns = [
    # --- Aportes do usuário (leitura) ---
    path('', views.aporte_list, name='aporte_list'),
    path('novo/', views.aporte_create, name='aporte_create'),
    path('<int:pk>/editar/', views.aporte_edit, name='aporte_edit'),
    path('<int:pk>/deletar/', views.aporte_delete, name='aporte_delete'),

    # --- Ativos do usuário (leitura) ---
    path('ativos/', views.ativo_list, name='ativo_list'),
    path('ativos/novo/', views.ativo_create, name='ativo_create'),
    path('ativos/<int:pk>/editar/', views.ativo_edit, name='ativo_edit'),
    path('ativos/<int:pk>/deletar/', views.ativo_delete, name='ativo_delete'),

    # --- Clientes (admin) ---
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/<int:user_pk>/', views.cliente_portfolio, name='cliente_portfolio'),
    path('clientes/<int:user_pk>/aportes/novo/', views.cliente_aporte_create, name='cliente_aporte_create'),
    path('clientes/<int:user_pk>/aportes/<int:pk>/editar/', views.cliente_aporte_edit, name='cliente_aporte_edit'),
    path('clientes/<int:user_pk>/aportes/<int:pk>/deletar/', views.cliente_aporte_delete, name='cliente_aporte_delete'),
    path('clientes/<int:user_pk>/ativos/novo/', views.cliente_ativo_create, name='cliente_ativo_create'),
    path('clientes/<int:user_pk>/ativos/<int:pk>/editar/', views.cliente_ativo_edit, name='cliente_ativo_edit'),
    path('clientes/<int:user_pk>/ativos/<int:pk>/deletar/', views.cliente_ativo_delete, name='cliente_ativo_delete'),

    # --- Categorias (admin) ---
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/deletar/', views.categoria_delete, name='categoria_delete'),

    # --- Dashboard (admin) ---
    path('dashboard/', views.dashboard, name='dashboard'),
]
