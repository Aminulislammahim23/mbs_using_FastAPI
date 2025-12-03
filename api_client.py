import requests

API_BASE = "http://127.0.0.1:8080"


def insert_account():
    try:
        acc_id = input("Enter Account ID: ")
        name = input("Enter Name: ")
        balance = float(input("Enter Initial Balance: "))

        payload = {
            "account_id": acc_id,
            "name": name,
            "balance": balance
        }

        response = requests.post(f"{API_BASE}/account/insert", json=payload)
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)


def update_account():
    try:
        acc_id = input("Enter Account ID to update: ")
        name = input("Enter new name: ")

        payload = {
            "account_id": acc_id,
            "name": name,
            "balance": 0  
        }

        response = requests.post(f"{API_BASE}/account/update", json=payload)
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)


def delete_account():
    try:
        acc_id = input("Enter Account ID to delete: ")
        response = requests.get(f"{API_BASE}/account/delete/{acc_id}")
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)

def show_accounts():
    try:
        response = requests.get(f"{API_BASE}/account/list")
        print("\nAll Accounts:", response.json()["accounts"])
    except Exception as e:
        print("Error:", e)

def deposit():
    try:
        acc_id = input("Enter Account ID: ")
        amount = float(input("Enter deposit amount: "))

        payload = {"account_id": acc_id, "amount": amount}
        response = requests.post(f"{API_BASE}/bank/deposit", json=payload)
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)



def withdraw():
    try:
        acc_id = input("Enter Account ID: ")
        amount = float(input("Enter withdraw amount: "))

        payload = {"account_id": acc_id, "amount": amount}
        response = requests.post(f"{API_BASE}/bank/withdraw", json=payload)
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)


def transfer():
    try:
        from_acc = input("From Account ID: ")
        to_acc = input("To Account ID: ")
        amount = float(input("Enter transfer amount: "))

        payload = {
            "from_acc": from_acc,
            "to_acc": to_acc,
            "amount": amount
        }
        response = requests.post(f"{API_BASE}/bank/transfer", json=payload)
    except Exception as e:
        print("Error:", e)


def show_transactions():
    try:
        response = requests.get(f"{API_BASE}/transactions")
        print("\nTransaction Logs:")
        for log in response.json()["logs"]:
            print(log.strip())
        print("\nResponse:", response.json())
    except Exception as e:
        print("Error:", e)


def menu():
    print("""
=====================================
        MICRO BANKING SYSTEM
=====================================
1. Insert Account
2. Update Account
3. Delete Account
4. Show All Accounts
5. Deposit
6. Withdraw
7. Transfer
8. Show Transactions
9. Exit
=====================================
""")


def main():
    while True:
        menu()
        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            insert_account()
        elif choice == "2":
            update_account()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            show_accounts()
        elif choice == "5":
            deposit()
        elif choice == "6":
            withdraw()
        elif choice == "7":
            transfer()
        elif choice == "8":
            show_transactions()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid option! Please choose correctly.")


if __name__ == "__main__":
    main()
