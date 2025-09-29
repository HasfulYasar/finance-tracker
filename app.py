from flask import Flask, render_template, request, redirect, session
from models import register_user, login_user, add_transaction, get_transactions

app = Flask(__name__)
app.secret_key = "some_secret_key"  # needed for session management

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
        if register_user(username, password):
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
    transactions = get_transactions(session["user_id"])
    return render_template("dashboard.html", username=session["username"], transactions=transactions)

# Add transaction
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

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
