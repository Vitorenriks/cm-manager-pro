import os
from flask import Flask
from flask_login import LoginManager
from models import init_db, get_db_connection, User
from routes import main

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')

# Inicializa o Banco
init_db()

# Configuração do Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login' # Note o 'main.' devido ao Blueprint

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'])
    return None

# Registra as rotas
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)