from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """Redireciona a raiz do site para a lista de aportes."""
    return redirect('aportes:aporte_list')
