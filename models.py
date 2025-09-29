from db import get_db_connection

# Register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Login a user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_transaction(user_id, amount, t_type, category, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, t_type, category, date)
    )
    conn.commit()
    conn.close()
    print("✅ Transaction added!")

def get_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, type, category, date FROM transactions WHERE user_id=?", (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions
