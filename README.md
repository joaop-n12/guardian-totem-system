# 🛡️ Smart Totem Security System

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![Cybersecurity](https://img.shields.io/badge/Sprint%203-Cybersecurity-red)

Este projeto foi desenvolvido para o **Entregável 3** com foco em aplicar controles fundamentais de segurança em uma aplicação Web Flask rodando em um Raspberry Pi. O sistema simula um totem inteligente, separando a interface pública de visualização das funções administrativas críticas (como o acionamento de atuadores/LED).

---

## 🚀 Funcionalidades e Critérios de Segurança Implementados

### 1. Controle de Acesso 👥
* **Tela Pública (`/`):** Acessível a qualquer usuário do totem para exibição de informações gerais.
* **Área Administrativa (`/admin`):** Restrita e protegida por autenticação. Bloqueia acessos diretos e redireciona tentativas não autorizadas para a tela de login.

### 2. Proteção de Credenciais e Configurações 🔐
* **Variáveis de Ambiente:** Utilização da biblioteca `python-dotenv` para carregar dados sensíveis (como `SECRET_KEY`, `ADMIN_USER` e `ADMIN_PASS`) a partir de um arquivo `.env`.
* **Segurança no Repositório:** O arquivo `.env` contendo as credenciais reais **foi adicionado ao `.gitignore`** para garantir que segredos nunca sejam expostos no histórico de versionamento (Git). No Raspberry Pi, esse arquivo é configurado localmente na pasta raiz da aplicação.

### 3. Proteção da Aplicação Web e Logs 🛡️
* **Validação de Entradas:** Tratamento básico no formulário de login para impedir submissões vazias.
* **Debug Desativado:** O modo de depuração do Flask foi explicitamente desativado (`debug=False`) em ambiente de produção para evitar o vazamento de stack traces e informações internas do servidor.
* **Mecanismo de Log (`/logs/app.log`):** Auditoria ativa usando a biblioteca nativa `logging`. O sistema registra:
  * Tentativas de login bem-sucedidas.
  * Tentativas de login inválidas (potenciais ataques de força bruta).
  * Tentativas de acesso negado a rotas restritas.
  * Execução de comandos administrativos (ex: acionamento do LED).

### 4. Controle Temporal da Sessão (Timeout) ⏱️
* Implementação de expiração automática da sessão baseada em inatividade. Se o administrador passar mais de 10 segundos sem interagir com a área restrita, a sessão é destruída (`session.clear()`) e o usuário é redirecionado para a tela inicial, simulando a perda de proximidade do usuário do totem.

---

## 🔧 Estrutura do Projeto

```text
smart-totem-security-system/
│
├── logs/
│   └── app.log          # Registro de auditoria e eventos de segurança
├── templates/
│   ├── index.html       # Tela pública do totem
│   ├── login.html       # Tela de autenticação admin
│   └── admin.html       # Painel administrativo protegido
├── .env                 # Arquivo local de credenciais (NÃO ENVIAR AO GIT)
├── .gitignore           # Bloqueador de arquivos sensíveis
├── app.py               # Código principal da aplicação Flask
└── requirements.txt     # Dependências do projeto

````


🛠️ Como Executar o Projeto
Pré-requisitos
Python 3.10 ou superior instalado.

Passo a Passo
Clone o repositório:

```
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```
Instale as dependências:
```
pip install -r requirements.txt
```
Configure as Variáveis de Ambiente:
Crie um arquivo chamado .env na raiz do projeto e adicione as seguintes chaves:
```
Code snippet
SECRET_KEY=sua_chave_secreta_aqui
ADMIN_USER=seu_usuario_admin
ADMIN_PASS=sua_senha_segura
```
Prepare a pasta de logs:
Certifique-se de que a pasta logs/ existe no diretório raiz. Se não, crie-a:
```
mkdir logs
```
Execute a aplicação:
```
python app.py
```
A aplicação estará disponível em http://127.0.0.1:5000/.
