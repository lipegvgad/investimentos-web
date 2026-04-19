# InvestTrack — Controle de Investimentos Pessoais

Sistema web para registro e acompanhamento de aportes em investimentos pessoais, desenvolvido em Python/Django como trabalho da disciplina INF1407 - Programação para Web (PUC-Rio, 2026/1).

## Componentes do grupo

- Luis Felipe Gadelha (2210308)

---

## O que foi desenvolvido

Site de controle de investimentos com dois perfis de acesso:

**Usuário comum** pode:
- Cadastrar, editar, visualizar e excluir seus **ativos** (ações, FIIs, ETFs, criptomoedas etc.)
- Registrar, editar, visualizar e excluir seus **aportes** (quantidade, preço unitário, data)
- Ver o total investido na listagem de aportes
- Criar conta, fazer login/logout e recuperar senha por e-mail

**Administrador** pode tudo isso e mais:
- Gerenciar **categorias** de ativos (CRUD exclusivo)
- Acessar o **dashboard** com totais consolidados de todos os usuários

---

## Como usar o site

### Rodando com Docker

```bash
# Clone o repositório
git clone https://github.com/lipegvgad/investimentos-web.git
cd investimentos-web

# Crie o arquivo .env com as credenciais de e-mail (necessário para recuperação de senha)
echo "EMAIL_HOST_USER=seuemail@gmail.com" >> .env
echo "EMAIL_HOST_PASSWORD=sua-senha-de-app-gmail" >> .env

# Suba os containers
docker-compose up --build
```

Acesse em: **http://localhost:8000**

### Criando o primeiro administrador

```bash
docker-compose exec web python manage.py createsuperuser
```

### Fluxo básico

1. Acesse `/usuarios/cadastro/` e crie uma conta
2. Faça login em `/usuarios/login/`
3. Vá em **Meus Ativos** e cadastre um ativo (ex: PETR4 — selecione uma categoria)
4. Vá em **Meus Aportes** e registre um aporte para esse ativo
5. O total investido aparece no rodapé da listagem

### Recuperação de senha

1. Na tela de login, clique em **Esqueceu a senha?**
2. Informe o e-mail cadastrado
3. Acesse o link recebido no e-mail para redefinir a senha

---

## O que funcionou

- CRUD completo de aportes, ativos e categorias
- Isolamento de dados por usuário (cada um vê apenas os próprios registros)
- Separação de permissões admin vs. usuário comum
- Recuperação de senha via e-mail (Gmail SMTP com App Password)
- Deploy com Docker + PostgreSQL + Gunicorn + WhiteNoise
- Interface responsiva sem uso de JavaScript

## O que não funcionou

- Não foi implementada a edição de perfil do usuário (alterar nome/e-mail pela interface do site)

---

## Publicação

A imagem Docker está disponível no Docker Hub:

```bash
docker pull lipegvgad/investtrack
docker-compose up
```

O repositório público está em: https://github.com/lipegvgad/investimentos-web
