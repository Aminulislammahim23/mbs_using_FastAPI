import requests

API_BASE = "http://127.0.0.1:8080"  # Micro Banking API server

# --------------------------
# CREATE ACCOUNT
# --------------------------
def create_account():
    try:
        name = input("Enter Account Holder Name: ")
        initial_balance = float(input("Enter Initial Balance: "))

        payload = {"name": name, "balance": initial_balance}
        response = requests.post(f"{API_BASE}/create_account", json=payload)
        result = response.json()

        print("\nResponse:", result)
        print("Account ID:", result["account_id"])
        print("Name:", result["name"])
        print("Balance:", result["balance"])
    except Exception as e:
        print("Error:", e)

# --------------------------
# CHECK BALANCE
# --------------------------
def check_balance():
    try:
        acc_id = input("Enter Account ID: ")

        response = requests.get(f"{API_BASE}/balance/{acc_id}")
        result = response.json()

        print("\nResponse:", result)
        print("Account ID:", result["account_id"])
        print("Balance:", result["balance"])
    except Exception as e:
        print("Error:", e)

# --------------------------
# DEPOSIT
# --------------------------
def deposit():
    try:
        acc_id = input("Enter Account ID: ")
        amount = float(input("Enter Deposit Amount: "))

        payload = {"amount": amount}
        response = requests.post(f"{API_BASE}/deposit/{acc_id}", json=payload)
        result = response.json()

        print("\nResponse:", result)
        print("New Balance:", result["new_balance"])
    except Exception as e:
        print("Error:", e)

# --------------------------
# WITHDRAW
# --------------------------
def withdraw():
    try:
        acc_id = input("Enter Account ID: ")
        amount = float(input("Enter Withdraw Amount: "))

        payload = {"amount": amount}
        response = requests.post(f"{API_BASE}/withdraw/{acc_id}", json=payload)
        result = response.json()

        print("\nResponse:", result)
        print("New Balance:", result["new_balance"])
    except Exception as e:
        print("Error:", e)

# --------------------------
# TRANSFER
# --------------------------
def transfer():
    try:
        from_acc = input("From Account ID: ")
        to_acc = input("To Account ID: ")
        amount = float(input("Enter Transfer Amount: "))

        payload = {
            "from_acc": from_acc,
            "to_acc": to_acc,
            "amount": amount
        }

        response = requests.post(f"{API_BASE}/transfer", json=payload)
        result = response.json()

        print("\nResponse:", result)
        print("From Account Balance:", result["from_balance"])
        print("To Account Balance:", result["to_balance"])
    except Exception as e:
        print("Error:", e)

# --------------------------
# MENU
# --------------------------
def menu():
    print("\n==============================")
    print("   MICRO BANKING CONSOLE MENU  ")
    print("==============================")
    print("1. Create Account")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Exit")
    print("==============================")

# --------------------------
# MAIN FUNCTION
# --------------------------
def main():
    while True:
        menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            check_balance()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            transfer()
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

if __name__ == "__main__":
    main()