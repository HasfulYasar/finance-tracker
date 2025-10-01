from flask import Flask, render_template, request, redirect, session
from models import register_user, login_user, add_transaction, get_transactions, get_categories, create_default_categories
from db import init_db

app = Flask(__name__)
app.secret_key = "some_secret_key"

# Initialize database when app starts
init_db()

# Home page
@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("login.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # register_user should return user_id if success
        user_id = register_user(username, password)
        if user_id:
            create_default_categories(user_id)  # attach default categories
            return redirect("/")
        else:
            return "Username already exists!"

    return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username, password)
        if user:
            session["user_id"] = user[0]  # user_id from DB
            session["username"] = username
            return redirect("/dashboard")
        else:
            return "Invalid credentials!"
    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    transactions = get_transactions(user_id)
    categories = get_categories(user_id)
    return render_template("dashboard.html", username=session["username"], transactions=transactions, categories=categories)

# Add transaction
@app.route("/add_transaction", methods=["POST"])
def add_trans():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    amount = float(request.form["amount"])
    t_type = request.form["type"]
    category = request.form["category"]
    date = request.form["date"]
    add_transaction(user_id, amount, t_type, category, date)
    return redirect("/dashboard")

# Manage categories (example page, you can build it)
@app.route("/categories")
def categories_page():
    if "user_id" not in session:
        return redirect("/")
    categories = get_categories(session["user_id"])
    return render_template("categories.html", categories=categories)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
