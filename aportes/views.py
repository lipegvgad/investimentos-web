from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .models import Categoria, Ativo, Aporte
from .forms import CategoriaForm, AtivoForm, AporteForm


# --- Decorator para views restritas a administradores ---

def admin_required(view_func):
    """Garante que apenas usuários is_staff acessem a view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('aportes:aporte_list')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


# ============================================================
# APORTES — CRUD do usuário comum
# ============================================================

@login_required
def aporte_list(request):
    """Lista todos os aportes do usuário logado, ordenados por data."""
    aportes = Aporte.objects.filter(usuario=request.user).select_related('ativo__categoria')
    total = aportes.aggregate(t=Sum('valor_total'))['t'] or 0
    return render(request, 'aportes/aporte_list.html', {
        'aportes': aportes,
        'total': total,
    })


@login_required
def aporte_create(request):
    """Cria um novo aporte para o usuário logado."""
    if request.method == 'POST':
        form = AporteForm(request.user, request.POST)
        if form.is_valid():
            aporte = form.save(commit=False)
            aporte.usuario = request.user  # vincula o aporte ao usuário logado
            aporte.save()
            messages.success(request, 'Aporte registrado com sucesso.')
            return redirect('aportes:aporte_list')
    else:
        form = AporteForm(request.user)
    return render(request, 'aportes/aporte_form.html', {
        'form': form,
        'titulo': 'Novo Aporte',
    })


@login_required
def aporte_edit(request, pk):
    """Edita um aporte existente — apenas o dono pode editar."""
    aporte = get_object_or_404(Aporte, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AporteForm(request.user, request.POST, instance=aporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aporte atualizado com sucesso.')
            return redirect('aportes:aporte_list')
    else:
        form = AporteForm(request.user, instance=aporte)
    return render(request, 'aportes/aporte_form.html', {
        'form': form,
        'titulo': 'Editar Aporte',
    })


@login_required
def aporte_delete(request, pk):
    """Exibe confirmação e deleta um aporte — página dedicada, sem JavaScript."""
    aporte = get_object_or_404(Aporte, pk=pk, usuario=request.user)
    if request.method == 'POST':
        aporte.delete()
        messages.success(request, 'Aporte removido com sucesso.')
        return redirect('aportes:aporte_list')
    return render(request, 'aportes/aporte_confirm_delete.html', {'objeto': aporte})


# ============================================================
# ATIVOS — CRUD do usuário comum
# ============================================================

@login_required
def ativo_list(request):
    """Lista os ativos cadastrados pelo usuário logado."""
    ativos = Ativo.objects.filter(usuario=request.user).select_related('categoria')
    return render(request, 'aportes/ativo_list.html', {'ativos': ativos})


@login_required
def ativo_create(request):
    """Cadastra um novo ativo para o usuário logado."""
    if request.method == 'POST':
        form = AtivoForm(request.POST)
        if form.is_valid():
            ativo = form.save(commit=False)
            ativo.usuario = request.user  # vincula o ativo ao usuário logado
            ativo.save()
            messages.success(request, 'Ativo cadastrado com sucesso.')
            return redirect('aportes:ativo_list')
    else:
        form = AtivoForm()
    return render(request, 'aportes/ativo_form.html', {
        'form': form,
        'titulo': 'Novo Ativo',
    })


@login_required
def ativo_edit(request, pk):
    """Edita um ativo — apenas o dono pode editar."""
    ativo = get_object_or_404(Ativo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AtivoForm(request.POST, instance=ativo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ativo atualizado com sucesso.')
            return redirect('aportes:ativo_list')
    else:
        form = AtivoForm(instance=ativo)
    return render(request, 'aportes/ativo_form.html', {
        'form': form,
        'titulo': 'Editar Ativo',
    })


@login_required
def ativo_delete(request, pk):
    """Confirmação de exclusão de ativo — página dedicada, sem JavaScript."""
    ativo = get_object_or_404(Ativo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        ativo.delete()
        messages.success(request, 'Ativo removido com sucesso.')
        return redirect('aportes:ativo_list')
    return render(request, 'aportes/ativo_confirm_delete.html', {'objeto': ativo})


# ============================================================
# CATEGORIAS — CRUD exclusivo de administradores
# ============================================================

@admin_required
def categoria_list(request):
    """Lista todas as categorias (somente admin)."""
    categorias = Categoria.objects.all()
    return render(request, 'aportes/categoria_list.html', {'categorias': categorias})


@admin_required
def categoria_create(request):
    """Cria uma nova categoria (somente admin)."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('aportes:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'aportes/categoria_form.html', {
        'form': form,
        'titulo': 'Nova Categoria',
    })


@admin_required
def categoria_edit(request, pk):
    """Edita uma categoria existente (somente admin)."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('aportes:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'aportes/categoria_form.html', {
        'form': form,
        'titulo': 'Editar Categoria',
    })


@admin_required
def categoria_delete(request, pk):
    """Confirmação de exclusão de categoria (somente admin)."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso.')
        return redirect('aportes:categoria_list')
    return render(request, 'aportes/categoria_confirm_delete.html', {'objeto': categoria})


# ============================================================
# DASHBOARD — Consolidado para administradores
# ============================================================

@admin_required
def dashboard(request):
    """Dashboard consolidado com totais por usuário, ativo e geral (somente admin)."""
    # Total investido agrupado por usuário
    por_usuario = (
        Aporte.objects
        .values('usuario__username')
        .annotate(total=Sum('valor_total'))
        .order_by('-total')
    )
    # Total investido agrupado por ativo
    por_ativo = (
        Aporte.objects
        .values('ativo__nome', 'ativo__ticker')
        .annotate(total=Sum('valor_total'))
        .order_by('-total')
    )
    # Soma geral de todos os aportes de todos os usuários
    total_geral = Aporte.objects.aggregate(t=Sum('valor_total'))['t'] or 0

    return render(request, 'aportes/dashboard.html', {
        'por_usuario': por_usuario,
        'por_ativo': por_ativo,
        'total_geral': total_geral,
    })
