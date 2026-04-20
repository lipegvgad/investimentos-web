from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

from .models import Categoria, Ativo, Aporte
from .forms import CategoriaForm, AtivoForm, AporteForm
from .utils import buscar_preco, gerar_grafico_donut


def admin_required(view_func):
    """Restringe acesso a usuários is_staff."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito ao gestor.')
            return redirect('aportes:aporte_list')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


# --- Visualização do cliente (somente leitura) ---

@login_required
def aporte_list(request):
    aportes = Aporte.objects.filter(usuario=request.user).select_related('ativo__categoria')
    total = aportes.aggregate(t=Sum('valor_total'))['t'] or 0
    por_tipo = aportes.values('ativo__tipo').annotate(total=Sum('valor_total')).order_by('-total')
    fatias = gerar_grafico_donut(por_tipo)
    return render(request, 'aportes/aporte_list.html', {
        'aportes': aportes,
        'total': total,
        'fatias': fatias,
    })


@login_required
def ativo_list(request):
    ativos = list(Ativo.objects.filter(usuario=request.user).select_related('categoria'))
    for ativo in ativos:
        ativo.preco_atual = buscar_preco(ativo.ticker, ativo.tipo)
        totais = Aporte.objects.filter(ativo=ativo).aggregate(tv=Sum('valor_total'), tq=Sum('quantidade'))
        if totais['tq']:
            ativo.preco_medio = float(totais['tv']) / float(totais['tq'])
            ativo.variacao = (ativo.preco_atual - ativo.preco_medio) / ativo.preco_medio * 100 if ativo.preco_atual else None
        else:
            ativo.preco_medio = None
            ativo.variacao = None
    return render(request, 'aportes/ativo_list.html', {'ativos': ativos})


# Rotas de escrita bloqueadas para clientes
@login_required
def aporte_create(request):
    messages.error(request, 'Apenas o gestor pode registrar aportes.')
    return redirect('aportes:aporte_list')

@login_required
def aporte_edit(request, pk):
    messages.error(request, 'Apenas o gestor pode editar aportes.')
    return redirect('aportes:aporte_list')

@login_required
def aporte_delete(request, pk):
    messages.error(request, 'Apenas o gestor pode remover aportes.')
    return redirect('aportes:aporte_list')

@login_required
def ativo_create(request):
    messages.error(request, 'Apenas o gestor pode cadastrar ativos.')
    return redirect('aportes:ativo_list')

@login_required
def ativo_edit(request, pk):
    messages.error(request, 'Apenas o gestor pode editar ativos.')
    return redirect('aportes:ativo_list')

@login_required
def ativo_delete(request, pk):
    messages.error(request, 'Apenas o gestor pode remover ativos.')
    return redirect('aportes:ativo_list')


# --- Gestão de clientes (somente gestor) ---

@admin_required
def cliente_list(request):
    clientes = list(User.objects.filter(is_staff=False).order_by('username'))
    for c in clientes:
        c.total_investido = Aporte.objects.filter(usuario=c).aggregate(t=Sum('valor_total'))['t'] or 0
    return render(request, 'aportes/cliente_list.html', {'clientes': clientes})


@admin_required
def cliente_portfolio(request, user_pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    aportes = Aporte.objects.filter(usuario=cliente).select_related('ativo__categoria')
    ativos = list(Ativo.objects.filter(usuario=cliente).select_related('categoria'))
    total = aportes.aggregate(t=Sum('valor_total'))['t'] or 0
    por_tipo = aportes.values('ativo__tipo').annotate(total=Sum('valor_total')).order_by('-total')
    fatias = gerar_grafico_donut(por_tipo)
    for ativo in ativos:
        ativo.preco_atual = buscar_preco(ativo.ticker, ativo.tipo)
        totais_a = Aporte.objects.filter(ativo=ativo).aggregate(tv=Sum('valor_total'), tq=Sum('quantidade'))
        if totais_a['tq']:
            ativo.preco_medio = float(totais_a['tv']) / float(totais_a['tq'])
            ativo.variacao = (ativo.preco_atual - ativo.preco_medio) / ativo.preco_medio * 100 if ativo.preco_atual else None
        else:
            ativo.preco_medio = None
            ativo.variacao = None
    return render(request, 'aportes/cliente_portfolio.html', {
        'cliente': cliente,
        'aportes': aportes,
        'ativos': ativos,
        'total': total,
        'fatias': fatias,
    })


@admin_required
def cliente_aporte_create(request, user_pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    if request.method == 'POST':
        form = AporteForm(cliente, request.POST)
        if form.is_valid():
            aporte = form.save(commit=False)
            aporte.usuario = cliente
            aporte.save()
            messages.success(request, 'Aporte registrado com sucesso.')
            return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    else:
        form = AporteForm(cliente)
    return render(request, 'aportes/aporte_form.html', {
        'form': form,
        'titulo': f'Novo Aporte — {cliente.username}',
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


@admin_required
def cliente_aporte_edit(request, user_pk, pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    aporte = get_object_or_404(Aporte, pk=pk, usuario=cliente)
    if request.method == 'POST':
        form = AporteForm(cliente, request.POST, instance=aporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aporte atualizado com sucesso.')
            return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    else:
        form = AporteForm(cliente, instance=aporte)
    return render(request, 'aportes/aporte_form.html', {
        'form': form,
        'titulo': f'Editar Aporte — {cliente.username}',
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


@admin_required
def cliente_aporte_delete(request, user_pk, pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    aporte = get_object_or_404(Aporte, pk=pk, usuario=cliente)
    if request.method == 'POST':
        aporte.delete()
        messages.success(request, 'Aporte removido com sucesso.')
        return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    return render(request, 'aportes/aporte_confirm_delete.html', {
        'objeto': aporte,
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


@admin_required
def cliente_ativo_create(request, user_pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    if request.method == 'POST':
        form = AtivoForm(request.POST)
        if form.is_valid():
            ativo = form.save(commit=False)
            ativo.usuario = cliente
            ativo.save()
            messages.success(request, 'Ativo cadastrado com sucesso.')
            return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    else:
        form = AtivoForm()
    return render(request, 'aportes/ativo_form.html', {
        'form': form,
        'titulo': f'Novo Ativo — {cliente.username}',
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


@admin_required
def cliente_ativo_edit(request, user_pk, pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    ativo = get_object_or_404(Ativo, pk=pk, usuario=cliente)
    if request.method == 'POST':
        form = AtivoForm(request.POST, instance=ativo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ativo atualizado com sucesso.')
            return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    else:
        form = AtivoForm(instance=ativo)
    return render(request, 'aportes/ativo_form.html', {
        'form': form,
        'titulo': f'Editar Ativo — {cliente.username}',
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


@admin_required
def cliente_ativo_delete(request, user_pk, pk):
    cliente = get_object_or_404(User, pk=user_pk, is_staff=False)
    ativo = get_object_or_404(Ativo, pk=pk, usuario=cliente)
    if request.method == 'POST':
        ativo.delete()
        messages.success(request, 'Ativo removido com sucesso.')
        return redirect('aportes:cliente_portfolio', user_pk=user_pk)
    return render(request, 'aportes/ativo_confirm_delete.html', {
        'objeto': ativo,
        'cancel_url': 'aportes:cliente_portfolio',
        'cancel_pk': user_pk,
    })


# --- Categorias e dashboard (somente gestor) ---

@admin_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'aportes/categoria_list.html', {'categorias': categorias})


@admin_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('aportes:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'aportes/categoria_form.html', {'form': form, 'titulo': 'Nova Categoria'})


@admin_required
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('aportes:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'aportes/categoria_form.html', {'form': form, 'titulo': 'Editar Categoria'})


@admin_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso.')
        return redirect('aportes:categoria_list')
    return render(request, 'aportes/categoria_confirm_delete.html', {'objeto': categoria})


@admin_required
def dashboard(request):
    por_usuario = (
        Aporte.objects
        .values('usuario__username')
        .annotate(total=Sum('valor_total'))
        .order_by('-total')
    )
    por_ativo = (
        Aporte.objects
        .values('ativo__nome', 'ativo__ticker')
        .annotate(total=Sum('valor_total'))
        .order_by('-total')
    )
    total_geral = Aporte.objects.aggregate(t=Sum('valor_total'))['t'] or 0
    return render(request, 'aportes/dashboard.html', {
        'por_usuario': por_usuario,
        'por_ativo': por_ativo,
        'total_geral': total_geral,
    })
