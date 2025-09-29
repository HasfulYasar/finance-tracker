import sqlite3, os

# Show which database file Python is using
db_path = os.path.abspath("finance.db")
print("Database in use:", db_path)

# Connect to database
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# Check structure of transactions table
cursor.execute("PRAGMA table_info(transactions)")
print("Transactions table schema:")
for col in cursor.fetchall():
    print(col)

conn.close()
