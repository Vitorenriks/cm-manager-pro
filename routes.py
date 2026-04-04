import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db_connection, User

main = Blueprint('main', __name__)

def get_placeholder():
    return "%s" if os.environ.get('DATABASE_URL') else "?"

@main.route('/register', methods=['GET', 'POST'])
def register():
    flash("Novos registros estão desativados no modo demonstração.", "warning")
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        p = get_placeholder()
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(f"SELECT id, username, password FROM users WHERE username = {p}", (username,))
            user = cur.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('main.dashboard'))
        flash("Login inválido.", "danger")
    return render_template('login.html')

@main.route('/')
@login_required
def dashboard():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM works")
        works = cur.fetchall()
    conn.close()
    return render_template("dashboard.html", works=works)

@main.route('/works/create', methods=['GET', 'POST'])
@login_required
def create_work():
    if request.method == 'POST':
        flash("Modo demonstração: criação de dados desativada.", "info")
        return redirect(url_for('main.dashboard'))
    return render_template("work_create.html")

@main.route('/works/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_work(id):
    if request.method == 'POST':
        flash("Modo demonstração: edição de dados desativada.", "info")
        return redirect(url_for('main.dashboard'))
    p = get_placeholder()
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM works WHERE id = {p}", (id,))
        work = cur.fetchone()
    conn.close()
    return render_template("work_edit.html", work=work)

@main.route('/works/<int:id>/delete', methods=['POST'])
@login_required
def delete_work(id):
    flash("Modo demonstração: exclusão de dados desativada.", "info")
    return redirect(url_for('main.dashboard'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for('main.login'))