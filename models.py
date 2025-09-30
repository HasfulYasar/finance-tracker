import sqlite3, os

DB_PATH = os.path.abspath("finance.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

# ------------------ USER FUNCTIONS ------------------ #
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None
    conn.close()
    return user_id

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# ------------------ TRANSACTIONS ------------------ #
def add_transaction(user_id, amount, t_type, category, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, t_type, category, date)
    )
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, type, category, date FROM transactions WHERE user_id=? ORDER BY date DESC", (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

# ------------------ CATEGORIES ------------------ #
def create_default_categories(user_id):
    defaults = [
        ("income", "Salary"),
        ("income", "Bonus"),
        ("expense", "Food"),
        ("expense", "Rent"),
        ("expense", "Bills"),
        ("expense", "Entertainment")
    ]
    conn = get_db_connection()
    cursor = conn.cursor()
    for t_type, name in defaults:
        cursor.execute("INSERT INTO categories (user_id, type, name) VALUES (?, ?, ?)", (user_id, t_type, name))
    conn.commit()
    conn.close()

def get_categories(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, name, type FROM categories WHERE user_id=?", (user_id,))
    cats = cursor.fetchall()
    conn.close()
    return cats

def add_category(user_id, name, t_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (user_id, type, name) VALUES (?, ?, ?)", (user_id, t_type, name))
    conn.commit()
    conn.close()

def edit_category(category_id, name, t_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET name=?, type=? WHERE category_id=?", (name, t_type, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id=?", (category_id,))
    conn.commit()
    conn.close()
