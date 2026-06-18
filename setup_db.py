import os
import sqlite3
from werkzeug.security import generate_password_hash

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

def init_db():
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        import psycopg2
        import psycopg2.extras

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        conn = psycopg2.connect(db_url, sslmode='require')
        conn.cursor_factory = psycopg2.extras.DictCursor
        cur = conn.cursor()

    else:
        conn = sqlite3.connect('works.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    p = "%s" if os.environ.get('DATABASE_URL') else "?"
    id_type = "SERIAL PRIMARY KEY" if os.environ.get('DATABASE_URL') else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS users (
            id {id_type},
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS works (
            id {id_type},
            user_id INTEGER,
            name TEXT NOT NULL,
            client TEXT NOT NULL,
            start_date TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    hashed = generate_password_hash(ADMIN_PASSWORD)
    cur.execute(f"SELECT id FROM users WHERE username = {p}", (ADMIN_USERNAME,))
    exists = cur.fetchone()

    if exists:
        cur.execute(
            f"UPDATE users SET password = {p} WHERE username = {p}",
            (hashed, ADMIN_USERNAME)
        )
    else:
        cur.execute(
            f"INSERT INTO users (username, password) VALUES ({p}, {p})",
            (ADMIN_USERNAME, hashed)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()