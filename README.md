# 🔐 Smart Totem Security System — Sprint 4

![Python](https://img.shields.io/badge/Python_3-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask_3.0-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![HTTPS](https://img.shields.io/badge/HTTPS-22c55e?style=flat-square&logo=letsencrypt&logoColor=white)
![RaspberryPi](https://img.shields.io/badge/Raspberry_Pi-A22846?style=flat-square&logo=raspberrypi&logoColor=white)

Sistema de totem inteligente com segurança aprimorada: HTTPS, proteção contra SQL Injection, rate limiting e hardening.

---

## 📋 Sobre o Projeto

O **Smart Totem Security System** é um sistema embarcado desenvolvido com Flask e Python, projetado para funcionar em um **Raspberry Pi** como totem interativo. Conta com uma **tela pública** exibindo informações de sensores em tempo real e uma **área administrativa** protegida por autenticação segura.

Esta Sprint evoluiu a segurança com comunicação criptografada via **HTTPS**, proteção contra **SQL Injection** e **força bruta**, além de correções de **hardening** identificadas na versão anterior.

---

## ⚙️ Instalação

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração do `.env`

Copie o exemplo e preencha com valores reais:

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Gere uma `SECRET_KEY` forte:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Exemplo de `.env` preenchido:

```env
SECRET_KEY=sua_chave_gerada_aqui
ADMIN_USER=admin
ADMIN_PASS=sua_senha_forte
```

> ⚠️ **Nunca commite o `.env` com valores reais.** Ele já está protegido pelo `.gitignore`.

---

## 🔒 Gerar certificado SSL (auto-assinado)

**Linux/Mac:**
```bash
chmod +x gerar_certificado.sh
./gerar_certificado.sh
```

**Windows (Git Bash):**
```bash
openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem \
  -days 365 -nodes -subj "//C=BR\ST=SP\CN=localhost"
```

---

## ▶️ Executar

```bash
python app.py
```

Acesse: **https://localhost:5000**

> O navegador vai exibir aviso de certificado auto-assinado. Clique em **"Avançado"** → **"Prosseguir para localhost"**.

---

## 🛡️ Segurança implementada

| Recurso | Descrição |
|---|---|
| **HTTPS** | Certificado auto-assinado via OpenSSL — toda comunicação criptografada via TLS |
| **Rate Limit** | Máx. 5 tentativas de login por minuto por IP — retorna HTTP 429 ao exceder |
| **Anti SQL Injection** | Consultas 100% parametrizadas com SQLite usando `?` — valores nunca interpolados |
| **Validação de input** | Limite de 50 chars e bloqueio de caracteres SQL (`'` `"` `;` `\`) |
| **Cabeçalhos HTTP** | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `HSTS` |
| **Sessão segura** | Timeout de 5 min, `SECRET_KEY` forte carregada via `.env` |
| **debug=False** | Modo produção ativo — erros internos não expostos ao cliente |
| **.gitignore** | `.env`, `certs/`, `*.db` e `logs/` fora do repositório |

---

## 🗂️ Rotas

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| `GET` | `/` | ❌ | Tela de loading |
| `GET` | `/home` | ❌ | Tela pública com leituras dos sensores |
| `GET/POST` | `/login` | ❌ | Autenticação administrativa *(rate limit: 5/min)* |
| `GET` | `/admin` | ✅ | Painel administrativo — requer sessão ativa |
| `GET` | `/ligar_led` | ✅ | Aciona o LED do totem |
| `GET` | `/logout` | ✅ | Encerra a sessão ativa |

---

## 🔧 Hardening aplicado

Vulnerabilidades identificadas na Sprint 3 e corrigidas nesta Sprint:

| Vulnerabilidade anterior | Correção aplicada |
|---|---|
| `SECRET_KEY=supersegredo123` hardcoded | Gerada com `secrets.token_hex(32)` via `.env` |
| Senha admin `1234` commitada no repositório | `.env` no `.gitignore` — nunca publicado |
| Sem validação de campos no login | `validar_input()` com limite de tamanho e bloqueio de chars SQL |
| Sem cabeçalhos de segurança HTTP | `X-Frame-Options`, `nosniff`, `HSTS` via `after_request` |
| Credencial admin em variável de ambiente | Admin criado no banco SQLite via `init_db()` |

---

## 📁 Estrutura

```
guardian-totem-system/
├── app.py                  ← aplicação principal
├── requirements.txt
├── .env.example            ← modelo de configuração (sem segredos)
├── .gitignore
├── gerar_certificado.sh
├── certs/                  ← gerado localmente, não commitado
│   ├── cert.pem
│   └── key.pem
├── logs/
│   └── app.log
├── totem.db                ← gerado ao iniciar, não commitado
└── templates/
    ├── loading.html
    ├── index.html
    ├── login.html
    └── admin.html
```

---

## 📦 Dependências

```
Flask==3.0.0
python-dotenv==1.0.1
Flask-Limiter==3.5.0
```

---

## 👤 Autor
 
**João Pedro de Souza Nunes**  
FIAP — Cyber Defense & Ethical Hacking · Sprint 4
