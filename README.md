# InvestTrack — Gestão de Portfólios de Investimentos

Sistema web para gestão de portfólios de investimentos, desenvolvido em Python/Django como trabalho da disciplina INF1407 - Programação para Web (PUC-Rio, 2026/1).

## Componentes do grupo

- Luis Felipe Gadelha (2210308)

---

## O que foi desenvolvido

O site simula uma plataforma de gestão de investimentos com dois perfis de acesso bem definidos:

**Gestor (administrador)** é o profissional responsável pelo portfólio dos clientes. Ele pode:
- Ver a lista de todos os clientes cadastrados com o total investido de cada um
- Acessar o portfólio completo de cada cliente
- Cadastrar, editar e excluir ativos e aportes de qualquer cliente
- Gerenciar as categorias de ativos disponíveis no sistema
- Visualizar o dashboard consolidado com totais por cliente e por ativo

**Cliente (usuário comum)** acessa o sistema apenas para acompanhar seu portfólio. Ele pode:
- Ver seus aportes e o total investido
- Ver seus ativos com o preço médio pago, preço atual (via API da B3) e variação percentual
- Visualizar o gráfico de distribuição do portfólio por tipo de ativo
- Criar conta, fazer login/logout e recuperar senha por e-mail

---

## Como usar o site

### Rodando com Docker

```bash
git clone https://github.com/lipegvgad/investimentos-web.git
cd investimentos-web

docker-compose up --build
```

Acesse em: **http://localhost:8000**

> **Funcionalidades opcionais:** o site funciona completamente sem configuração extra. Duas funcionalidades dependem de credenciais externas:
> - **Preços em tempo real** (Brapi.dev): crie um `.env` com `BRAPI_TOKEN=seu-token`. Sem ele, a coluna de preço atual exibe "—".
> - **Recuperação de senha por e-mail** (Gmail): adicione `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` ao `.env`. Sem isso, o restante do site funciona normalmente.

### Criando o gestor

```bash
docker-compose exec web python manage.py createsuperuser
```

### Fluxo do gestor

1. Faça login com a conta de gestor
2. Acesse **Clientes** na barra lateral
3. Clique em **Ver Portfólio** de um cliente
4. Cadastre ativos e registre aportes para esse cliente

### Fluxo do cliente

1. Acesse `/usuarios/cadastro/` e crie uma conta
2. Faça login — o gestor cadastrará os ativos e aportes para você
3. Acompanhe seu portfólio em **Meus Aportes** e **Meus Ativos**

### Recuperação de senha

1. Na tela de login, clique em **Esqueceu a senha?**
2. Informe o e-mail cadastrado
3. Acesse o link recebido no e-mail para criar uma nova senha

---

## O que funcionou

- CRUD completo de aportes, ativos e categorias (operado pelo gestor)
- Separação de perfis: gestor com acesso total, cliente somente leitura
- Preço atual dos ativos em tempo real via API Brapi.dev (B3)
- Cálculo de preço médio pago e variação percentual por ativo
- Gráfico de distribuição do portfólio por tipo de ativo (SVG gerado pelo servidor, sem JavaScript)
- Validação de ticker de ações e FIIs contra a API da B3 no momento do cadastro
- Recuperação de senha via e-mail (Gmail SMTP com App Password)
- Deploy com Docker + PostgreSQL + Gunicorn + WhiteNoise
- Interface sem uso de JavaScript

## O que não funcionou

- Não foi implementada a edição de perfil do usuário (alterar nome ou e-mail pela interface do site)

---

## Publicação

A imagem Docker está disponível no Docker Hub: https://hub.docker.com/r/lipegvgad/investtrack

```bash
docker pull lipegvgad/investtrack
docker-compose up
```

O repositório público está em: https://github.com/lipegvgad/investimentos-web
