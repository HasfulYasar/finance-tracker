from models import register_user, login_user, add_transaction, get_transactions

print("=== Personal Finance Tracker ===")

while True:
    choice = input("1. Register\n2. Login\n3. Exit\nChoose: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        if register_user(username, password):
            print("✅ User registered!")
        else:
            print("❌ Registration failed (username may already exist).")

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        user = login_user(username, password)
        if user:
            print(f"✅ Welcome {username}!")
            user_id = user[0]  # first column in 'users' table = user_id

            # Sub-menu for transactions
            while True:
                sub_choice = input("\n1. Add Transaction\n2. View Transactions\n3. Logout\nChoose: ")

                if sub_choice == "1":
                    amount = float(input("Amount: "))
                    t_type = input("Type (income/expense): ")
                    category = input("Category: ")
                    date = input("Date (YYYY-MM-DD): ")
                    add_transaction(user_id, amount, t_type, category, date)

                elif sub_choice == "2":
                    transactions = get_transactions(user_id)
                    for t in transactions:
                        print(t)

                elif sub_choice == "3":
                    print("Logged out!")
                    break
                else:
                    print("Invalid choice.")

        else:
            print("❌ Invalid credentials.")

    elif choice == "3":
        break

    else:
        print("Invalid choice.")
