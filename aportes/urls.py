from django.urls import path
from . import views

app_name = 'aportes'

urlpatterns = [
    # --- Aportes ---
    path('', views.aporte_list, name='aporte_list'),
    path('novo/', views.aporte_create, name='aporte_create'),
    path('<int:pk>/editar/', views.aporte_edit, name='aporte_edit'),
    path('<int:pk>/deletar/', views.aporte_delete, name='aporte_delete'),

    # --- Ativos ---
    path('ativos/', views.ativo_list, name='ativo_list'),
    path('ativos/novo/', views.ativo_create, name='ativo_create'),
    path('ativos/<int:pk>/editar/', views.ativo_edit, name='ativo_edit'),
    path('ativos/<int:pk>/deletar/', views.ativo_delete, name='ativo_delete'),

    # --- Categorias (admin) ---
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/deletar/', views.categoria_delete, name='categoria_delete'),

    # --- Dashboard (admin) ---
    path('dashboard/', views.dashboard, name='dashboard'),
]
