import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Em produção, use uma variável de ambiente. Para desenvolvimento, esta chave assina os cookies de sessão.
app.config['SECRET_KEY'] = 'dev_key_123_construction_management'

# --- CONFIGURAÇÃO DO FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona para aqui se tentar acessar algo restrito
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"

# Modelo de Usuário para o Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('works.db')
    user = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hashing de senha - Padrão de segurança exigido em auditorias
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            conn = sqlite3.connect('works.db')
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            flash("Conta criada com sucesso! Você já pode entrar.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Este nome de usuário já está em uso.", "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('works.db')
        user = conn.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        # Verifica se o usuário existe e se a senha "bate" com o hash
        if user and check_password_hash(user[2], password):
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            flash(f"Bem-vindo de volta, {username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login inválido. Verifique usuário e senha.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for('login'))

# --- ROTAS DO DASHBOARD (CRUD) ---

@app.route('/')
@login_required # Só acessa quem estiver logado
def dashboard():
    conn = sqlite3.connect('works.db')
    conn.row_factory = sqlite3.Row
    # Opcional: Filtrar apenas obras do usuário logado no futuro
    works = conn.execute("SELECT * FROM works").fetchall()
    conn.close()
    return render_template("dashboard.html", works=works)

@app.route('/works/create', methods=['GET', 'POST'])
@login_required
def create_work():
    if request.method == 'POST':
        name = request.form['name']
        client = request.form['client']
        start_date = request.form['start_date']
        status = request.form['status']

        conn = sqlite3.connect('works.db')
        conn.execute("INSERT INTO works (name, client, start_date, status) VALUES (?, ?, ?, ?)",
                     (name, client, start_date, status))
        conn.commit()
        conn.close()
        flash("Obra cadastrada com sucesso!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template("work_create.html")

@app.route('/works/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_work(id):
    conn = sqlite3.connect('works.db')
    conn.row_factory = sqlite3.Row
    work = conn.execute("SELECT * FROM works WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        client = request.form['client']
        start_date = request.form['start_date']
        status = request.form['status']

        conn.execute("UPDATE works SET name = ?, client = ?, start_date = ?, status = ? WHERE id = ?",
                     (name, client, start_date, status, id))
        conn.commit()
        conn.close()
        flash("Dados atualizados!", "success")
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template("work_edit.html", work=work)

@app.route('/works/<int:id>/delete', methods=['POST'])
@login_required
def delete_work(id):
    conn = sqlite3.connect('works.db')
    conn.execute("DELETE FROM works WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Obra removida do sistema.", "warning")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)