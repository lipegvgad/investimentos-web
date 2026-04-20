import os
import math
import requests

_TIPOS_B3 = {'acao', 'fii'}
_BRAPI_URL = "https://brapi.dev/api/quote/{ticker}"

_CORES_TIPO = {
    'acao':       '#4299e1',
    'fii':        '#48bb78',
    'renda_fixa': '#ed8936',
    'cripto':     '#9f7aea',
    'outro':      '#718096',
}

_LABELS_TIPO = {
    'acao':       'Ações',
    'fii':        'FIIs',
    'renda_fixa': 'Renda Fixa',
    'cripto':     'Criptomoedas',
    'outro':      'Outros',
}


def buscar_preco(ticker, tipo):
    if not ticker or tipo not in _TIPOS_B3:
        return None
    try:
        token = os.environ.get('BRAPI_TOKEN', '')
        params = {'token': token} if token else {}
        resp = requests.get(_BRAPI_URL.format(ticker=ticker), params=params, timeout=5)
        data = resp.json()
        if data.get('error'):
            return None
        results = data.get('results', [])
        return results[0].get('regularMarketPrice') if results else None
    except Exception:
        return None


def gerar_grafico_donut(por_tipo, cx=110, cy=110, r_ext=90, r_int=52):
    total = sum(float(d['total']) for d in por_tipo)
    if not total:
        return []

    fatias = []
    angulo = -math.pi / 2

    for d in por_tipo:
        tipo = d['ativo__tipo']
        valor = float(d['total'])
        pct = valor / total
        angulo_fim = angulo + 2 * math.pi * pct

        x1e = cx + r_ext * math.cos(angulo)
        y1e = cy + r_ext * math.sin(angulo)
        x2e = cx + r_ext * math.cos(angulo_fim)
        y2e = cy + r_ext * math.sin(angulo_fim)
        x1i = cx + r_int * math.cos(angulo_fim)
        y1i = cy + r_int * math.sin(angulo_fim)
        x2i = cx + r_int * math.cos(angulo)
        y2i = cy + r_int * math.sin(angulo)

        large = 1 if pct > 0.5 else 0

        path = (
            f"M {x1e:.2f} {y1e:.2f} "
            f"A {r_ext} {r_ext} 0 {large} 1 {x2e:.2f} {y2e:.2f} "
            f"L {x1i:.2f} {y1i:.2f} "
            f"A {r_int} {r_int} 0 {large} 0 {x2i:.2f} {y2i:.2f} Z"
        )

        fatias.append({
            'path': path,
            'cor': _CORES_TIPO.get(tipo, '#718096'),
            'label': _LABELS_TIPO.get(tipo, tipo),
            'pct': pct * 100,
            'total': valor,
        })

        angulo = angulo_fim

    return fatias
