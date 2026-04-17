# Imagem base leve com Python 3.9
FROM python:3.9-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências antes de copiar o código (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Coleta os arquivos estáticos para o diretório staticfiles/
RUN python manage.py collectstatic --noinput

# Porta exposta pelo gunicorn
EXPOSE 8000

# Inicia o servidor de produção
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
