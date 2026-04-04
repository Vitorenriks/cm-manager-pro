import sqlite3
import psycopg2
import psycopg2.extras
import os
from flask_login import UserMixin

DATABASE = 'works.db'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        conn = psycopg2.connect(db_url, sslmode='require')
        conn.cursor_factory = psycopg2.extras.DictCursor
        return conn
    else:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    db_url = os.environ.get('DATABASE_URL')
    conn = get_db_connection()
    id_type = "SERIAL PRIMARY KEY" if db_url else "INTEGER PRIMARY KEY AUTOINCREMENT"
    
    with conn.cursor() as cur:
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
                name TEXT NOT NULL,
                client TEXT NOT NULL,
                start_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()