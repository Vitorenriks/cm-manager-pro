import sqlite3

def init_db():
    conn = sqlite3.connect('works.db')
    cursor = conn.cursor()

    print("Iniciando atualização do banco de dados...")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

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