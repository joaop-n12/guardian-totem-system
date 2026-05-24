# 🔐 Smart Totem Security System — Sprint 4

Sistema de totem inteligente com segurança aprimorada: HTTPS, proteção contra SQL Injection, rate limiting e hardening.

---

## ⚙️ Instalação

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração do .env

Copie o exemplo e preencha com valores reais:

```bash
cp .env.example .env
```

Gere uma SECRET_KEY forte:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🔒 Gerar certificado SSL (auto-assinado)

```bash
chmod +x gerar_certificado.sh
./gerar_certificado.sh
```

---

## ▶️ Executar

```bash
python app.py
```

Acesse: **https://localhost:5000**

> O navegador vai exibir aviso de certificado auto-assinado. Clique em "Avançado" → "Prosseguir para localhost".

---

## 🛡️ Segurança implementada

| Recurso | Descrição |
|---|---|
| **HTTPS** | Certificado auto-assinado via OpenSSL |
| **Rate Limit** | Máx. 5 tentativas de login por minuto por IP |
| **SQL Injection** | Consultas parametrizadas com SQLite (`?`) |
| **Validação de input** | Limite de 50 chars, bloqueio de caracteres SQL |
| **Cabeçalhos HTTP** | X-Frame-Options, X-Content-Type-Options, HSTS |
| **Sessão segura** | Timeout de 5 min, SECRET_KEY via .env |
| **debug=False** | Modo produção sem exposição de erros internos |
| **.gitignore** | .env, certs/ e .db fora do repositório |

---

## 📁 Estrutura

```
smart-totem-security-system/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── gerar_certificado.sh
├── certs/          ← gerado localmente, não commitado
├── logs/
│   └── app.log
├── totem.db        ← gerado ao iniciar, não commitado
└── templates/
    ├── loading.html
    ├── index.html
    ├── login.html
    └── admin.html
```
