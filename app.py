from flask import Flask, render_template, request, redirect, session, jsonify
import os
import sqlite3
import re
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ─────────────────────────────────────────
# Segurança: cabeçalhos HTTP (hardening)
# ─────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

# ─────────────────────────────────────────
# Rate Limit
# ─────────────────────────────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "60 per hour"],
    storage_uri="memory://"
)

SESSION_TIMEOUT = 300  # 5 minutos

# ─────────────────────────────────────────
# Logging
# ─────────────────────────────────────────
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# ─────────────────────────────────────────
# Banco de dados SQLite (consultas parametrizadas)
# ─────────────────────────────────────────
def init_db():
    """Inicializa o banco e cria tabela de usuários se não existir."""
    conn = sqlite3.connect('totem.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')
    # Insere admin padrão só se ainda não existir
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASS")
    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (admin_user,)
    )
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (admin_user, admin_pass, "admin")
        )
    conn.commit()
    conn.close()


def buscar_usuario(username, password):
    """
    Busca usuário usando consulta parametrizada (prevenção de SQL Injection).
    Nunca concatena strings — valores são passados como parâmetros separados.
    """
    conn = sqlite3.connect('totem.db')
    cursor = conn.cursor()
    # ✅ SEGURO: parâmetros ? nunca são interpolados diretamente na query
    cursor.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def validar_input(valor, max_len=50):
    """Valida se o input é string não vazia, sem caracteres especiais perigosos e dentro do limite."""
    if not valor or not isinstance(valor, str):
        return False
    if len(valor) > max_len:
        return False
    # Bloqueia caracteres SQL mais usados em injeção
    if re.search(r"['\";\\]", valor):
        return False
    return True


# ─────────────────────────────────────────
# Rotas
# ─────────────────────────────────────────
@app.route('/')
def loading():
    return render_template('loading.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # ✅ Rate limit: máx 5 tentativas/minuto por IP
def login():
    erro = None

    if request.method == 'POST':
        user = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Validação de input (hardening)
        if not validar_input(user) or not validar_input(password):
            erro = "Entrada inválida. Verifique os campos."
            logging.warning(f"Input inválido no login - IP: {request.remote_addr}")
        else:
            resultado = buscar_usuario(user, password)

            if resultado:
                session['user'] = resultado[0]
                session['role'] = resultado[1]
                session['last_activity'] = datetime.now().isoformat()
                logging.info(f"Login bem-sucedido: {user} - IP: {request.remote_addr}")
                return redirect('/admin')
            else:
                erro = "Usuário ou senha inválidos"
                logging.warning(f"Tentativa de login inválida: {user} - IP: {request.remote_addr}")

    return render_template('login.html', erro=erro)


@app.errorhandler(429)
def ratelimit_error(e):
    logging.warning(f"Rate limit atingido - IP: {request.remote_addr}")
    return render_template('login.html', erro="Muitas tentativas. Aguarde 1 minuto."), 429


@app.route('/admin')
def admin():
    if 'user' not in session:
        logging.warning(f"Acesso negado à área admin - IP: {request.remote_addr}")
        return redirect('/login')

    last_activity = datetime.fromisoformat(session['last_activity'])
    if datetime.now() - last_activity > timedelta(seconds=SESSION_TIMEOUT):
        session.clear()
        logging.info("Sessão expirada por inatividade")
        return redirect('/login')

    session['last_activity'] = datetime.now().isoformat()
    return render_template('admin.html', usuario=session['user'])


@app.route('/ligar_led')
def ligar_led():
    if 'user' not in session:
        logging.warning(f"Tentativa sem sessão (LED) - IP: {request.remote_addr}")
        return redirect('/login')

    logging.info(f"LED acionado por: {session['user']}")
    return "LED LIGADO ✅"


@app.route('/logout')
def logout():
    usuario = session.get('user', 'desconhecido')
    session.clear()
    logging.info(f"Logout: {usuario}")
    return redirect('/home')


# ─────────────────────────────────────────
# Inicialização
# ─────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # ✅ debug=False em produção (hardening)
        ssl_context=('certs/cert.pem', 'certs/key.pem')  # ✅ HTTPS com certificado local
    )
