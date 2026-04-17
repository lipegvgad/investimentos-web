from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Ativo(models.Model):
    TIPO_CHOICES = [
        ('acao', 'Ação'),
        ('fii', 'FII'),
        ('renda_fixa', 'Renda Fixa'),
        ('cripto', 'Criptomoeda'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    ticker = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='ativos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ativos')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'

    def __str__(self):
        return f'{self.ticker} - {self.nome}' if self.ticker else self.nome


class Aporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aportes')
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT, related_name='aportes')
    data = models.DateField()
    quantidade = models.DecimalField(max_digits=15, decimal_places=6)
    preco_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Aporte'
        verbose_name_plural = 'Aportes'

    def clean(self):
        if self.data and self.data > timezone.localdate():
            raise ValidationError({'data': 'A data do aporte não pode ser futura.'})
        if self.quantidade is not None and self.quantidade <= 0:
            raise ValidationError({'quantidade': 'A quantidade deve ser positiva.'})
        if self.preco_unitario is not None and self.preco_unitario <= 0:
            raise ValidationError({'preco_unitario': 'O preço unitário deve ser positivo.'})

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.username} - {self.ativo} - {self.data}'
