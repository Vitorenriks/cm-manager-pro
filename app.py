import os
from flask import Flask
from flask_login import LoginManager
from models import init_db, get_db_connection, User 
from routes import main

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')

uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['DATABASE_URL'] = uri or 'sqlite:///database.db'

# Inicializa o banco de dados
init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    db_url = os.environ.get('DATABASE_URL')
    p = "%s" if db_url else "?"
    
    user = None
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT id, username FROM users WHERE id = {p}", (user_id,))
            row = cur.fetchone()
            if row:
                user = User(row[0], row[1])
    finally:
        conn.close()
    return user

app.register_blueprint(main)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)