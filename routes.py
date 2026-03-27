import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db_connection, User

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError:
            flash("Este nome de usuário já está em uso.", "danger")
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            flash(f"Bem-vindo, {username}!", "success")
            return redirect(url_for('main.dashboard'))
        flash("Login inválido.", "danger")
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def dashboard():
    conn = get_db_connection()
    works = conn.execute("SELECT * FROM works").fetchall()
    conn.close()
    return render_template("dashboard.html", works=works)

@main.route('/works/create', methods=['GET', 'POST'])
@login_required
def create_work():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("INSERT INTO works (name, client, start_date, status) VALUES (?, ?, ?, ?)",
                     (request.form['name'], request.form['client'], request.form['start_date'], request.form['status']))
        conn.commit()
        conn.close()
        flash("Obra cadastrada!", "success")
        return redirect(url_for('main.dashboard'))
    return render_template("work_create.html")

@main.route('/works/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_work(id):
    conn = get_db_connection()
    work = conn.execute("SELECT * FROM works WHERE id = ?", (id,)).fetchone()
    if request.method == 'POST':
        conn.execute("UPDATE works SET name = ?, client = ?, start_date = ?, status = ? WHERE id = ?",
                     (request.form['name'], request.form['client'], request.form['start_date'], request.form['status'], id))
        conn.commit()
        conn.close()
        return redirect(url_for('main.dashboard'))
    conn.close()
    return render_template("work_edit.html", work=work)

@main.route('/works/<int:id>/delete', methods=['POST'])
@login_required
def delete_work(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM works WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('main.dashboard'))