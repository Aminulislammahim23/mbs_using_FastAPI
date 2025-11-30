from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

ACCOUNTS_FILE = "data/accounts.txt"
TRANSACTION_FILE = "data/transactions.txt"


class AccountModel(BaseModel):
    account_id: str
    name: str
    balance: float


class DepositWithdrawModel(BaseModel):
    account_id: str
    amount: float


class TransferModel(BaseModel):
    from_acc: str
    to_acc: str
    amount: float


def read_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return []

    with open(ACCOUNTS_FILE, "r") as file:
        lines = file.readlines()

    accounts = []
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) == 3:
            accounts.append({
                "account_id": parts[0],
                "name": parts[1],
                "balance": float(parts[2])
            })

    return accounts


def write_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        for acc in accounts:
            file.write(f"{acc['account_id']}|{acc['name']}|{acc['balance']}\n")


def log_transaction(text):
    with open(TRANSACTION_FILE, "a") as file:
        file.write(text + "\n")


@app.post("/account/insert")
def insert_account(acc: AccountModel):
    accounts = read_accounts()

    for a in accounts:
        if a["account_id"] == acc.account_id:
            return {"error": "Account ID already exists"}

    accounts.append(acc.dict())
    write_accounts(accounts)

    return {"message": "Account inserted successfully"}


@app.post("/account/update")
def update_account(acc: AccountModel):
    accounts = read_accounts()
    updated = False

    for a in accounts:
        if a["account_id"] == acc.account_id:
            a["name"] = acc.name
            updated = True

    if not updated:
        return {"error": "Account not found"}

    write_accounts(accounts)
    return {"message": "Account updated successfully"}


@app.get("/account/delete/{acc_id}")
def delete_account(acc_id: str):
    accounts = read_accounts()
    new_list = [a for a in accounts if a["account_id"] != acc_id]

    if len(new_list) == len(accounts):
        return {"error": "Account not found"}

    write_accounts(new_list)
    return {"message": "Account deleted successfully"}


@app.get("/account/list")
def list_accounts():
    return {"accounts": read_accounts()}


@app.post("/bank/deposit")
def deposit(data: DepositWithdrawModel):
    accounts = read_accounts()

    for a in accounts:
        if a["account_id"] == data.account_id:
            a["balance"] += data.amount
            write_accounts(accounts)
            log_transaction(f"DEPOSIT | {data.account_id} | +{data.amount}")
            return {"message": "Deposit successful"}

    return {"error": "Account not found"}


@app.post("/bank/withdraw")
def withdraw(data: DepositWithdrawModel):
    accounts = read_accounts()

    for a in accounts:
        if a["account_id"] == data.account_id:

            if a["balance"] < data.amount:
                return {"error": "Insufficient balance"}

            a["balance"] -= data.amount
            write_accounts(accounts)
            log_transaction(f"WITHDRAW | {data.account_id} | -{data.amount}")
            return {"message": "Withdrawal successful"}

    return {"error": "Account not found"}


@app.post("/bank/transfer")
def transfer(data: TransferModel):
    accounts = read_accounts()

    sender = None
    receiver = None

    for a in accounts:
        if a["account_id"] == data.from_acc:
            sender = a
        if a["account_id"] == data.to_acc:
            receiver = a

    if sender is None:
        return {"error": "Sender not found"}
    if receiver is None:
        return {"error": "Receiver not found"}
    if sender["balance"] < data.amount:
        return {"error": "Insufficient balance"}

    sender["balance"] -= data.amount
    receiver["balance"] += data.amount
    write_accounts(accounts)

    log_transaction(f"TRANSFER | {data.from_acc} -> {data.to_acc} | {data.amount}")

    return {"message": "Transfer successful"}


@app.get("/transactions")
def show_logs():
    if not os.path.exists(TRANSACTION_FILE):
        return {"logs": []}

    with open(TRANSACTION_FILE, "r") as file:
        lines = file.readlines()

    return {"logs": lines}

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8080, reload=True)
