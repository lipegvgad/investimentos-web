from django import forms
from django.utils import timezone
from .models import Categoria, Ativo, Aporte


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']


class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['nome', 'ticker', 'tipo', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['ticker'].required = False


class AporteForm(forms.ModelForm):
    class Meta:
        model = Aporte
        fields = ['ativo', 'data', 'quantidade', 'preco_unitario']
        widgets = {
            # Usa o seletor de data nativo do navegador (sem JavaScript)
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas os ativos do usuário logado
        self.fields['ativo'].queryset = Ativo.objects.filter(usuario=user).select_related('categoria')
        # Garante que o campo data use o formato correto
        self.fields['data'].input_formats = ['%Y-%m-%d']

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > timezone.localdate():
            raise forms.ValidationError('A data do aporte não pode ser futura.')
        return data

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is not None and quantidade <= 0:
            raise forms.ValidationError('A quantidade deve ser positiva.')
        return quantidade

    def clean_preco_unitario(self):
        preco = self.cleaned_data.get('preco_unitario')
        if preco is not None and preco <= 0:
            raise forms.ValidationError('O preço unitário deve ser positivo.')
        return preco
