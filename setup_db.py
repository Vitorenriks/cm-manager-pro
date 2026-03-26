import sqlite3

def init_db():
    conn = sqlite3.connect('works.db')
    cursor = conn.cursor()

    print("Iniciando atualização do banco de dados...")

    # 1. Criar tabela de usuários (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Garantir que a tabela de obras (works) existe
    # Adicionamos a coluna user_id para que no futuro cada obra pertença a um dono
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            client TEXT NOT NULL,
            start_date TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ SQLite!")

if __name__ == "__main__":
    init_db()