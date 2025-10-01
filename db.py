import sqlite3
import os

DB_PATH = os.path.abspath("finance.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # optional, allows dict-like access
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,  -- income or expense
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized at:", DB_PATH)
