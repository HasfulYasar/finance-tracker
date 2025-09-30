from flask import Flask, render_template, request, redirect, session
from models import (
    register_user, login_user, add_transaction, get_transactions,
    create_default_categories, get_categories, add_category, edit_category, delete_category
)

app = Flask(__name__)
app.secret_key = "some_secret_key"

# ------------------ HOME ------------------ #
@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("login.html")

# ------------------ REGISTER ------------------ #
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = register_user(username, password)
        if user_id:
            create_default_categories(user_id)  # Add default categories
            return redirect("/")
        else:
            return "Username already exists!"
    return render_template("register.html")

# ------------------ LOGIN ------------------ #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username, password)
        if user:
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/dashboard")
        else:
            return "Invalid credentials!"
    return render_template("login.html")

# ------------------ DASHBOARD ------------------ #
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    transactions = get_transactions(session["user_id"])
    categories = get_categories(session["user_id"])
    return render_template("dashboard.html", username=session["username"], transactions=transactions, categories=categories)

# ------------------ ADD TRANSACTION ------------------ #
@app.route("/add_transaction", methods=["POST"])
def add_trans():
    if "user_id" not in session:
        return redirect("/")
    amount = float(request.form["amount"])
    t_type = request.form["type"]
    category = request.form["category"]
    date = request.form["date"]
    add_transaction(session["user_id"], amount, t_type, category, date)
    return redirect("/dashboard")

# ------------------ MANAGE CATEGORIES ------------------ #
@app.route("/categories", methods=["GET", "POST"])
def manage_categories():
    if "user_id" not in session:
        return redirect("/")
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form["name"]
            t_type = request.form["type"]
            add_category(session["user_id"], name, t_type)
        elif action == "edit":
            category_id = int(request.form["category_id"])
            name = request.form["name"]
            t_type = request.form["type"]
            edit_category(category_id, name, t_type)
        elif action == "delete":
            category_id = int(request.form["category_id"])
            delete_category(category_id)
        return redirect("/categories")
    categories = get_categories(session["user_id"])
    return render_template("categories.html", categories=categories)

# ------------------ LOGOUT ------------------ #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
