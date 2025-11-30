from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import uuid

app = FastAPI(title="Micro Banking System API")

accounts = {}

class CreateAccountModel(BaseModel):
    name: str
    initial_balance: float

class AmountModel(BaseModel):
    amount: float


class TransferModel(BaseModel):
    from_acc: str
    to_acc: str
    amount: float
# Create Account
# -----------------------------
@app.post("/create_account")
def create_account(data: CreateAccountModel):
    acc_id = str(uuid.uuid4())  # unique account id
    accounts[acc_id] = {
        "name": data.name,
        "balance": data.balance
    }

    return {
        "message": "Account created successfully",
        "account_id": acc_id,
        "name": data.name,
        "balance": data.balance
    }


# -----------------------------
# Check Balance
# -----------------------------
@app.get("/balance/{acc_id}")
def check_balance(acc_id: str):
    if acc_id not in accounts:
        return {"error": "Account not found"}

    return {
        "account_id": acc_id,
        "balance": accounts[acc_id]["balance"]
    }


# -----------------------------
# Deposit
# -----------------------------
@app.post("/deposit/{acc_id}")
def deposit(acc_id: str, data: AmountModel):
    if acc_id not in accounts:
        return {"error": "Account not found"}

    accounts[acc_id]["balance"] += data.amount

    return {
        "message": "Deposit successful",
        "account_id": acc_id,
        "new_balance": accounts[acc_id]["balance"]
    }


# -----------------------------
# Withdraw
# -----------------------------
@app.post("/withdraw/{acc_id}")
def withdraw(acc_id: str, data: AmountModel):
    if acc_id not in accounts:
        return {"error": "Account not found"}

    if accounts[acc_id]["balance"] < data.amount:
        return {"error": "Insufficient balance"}

    accounts[acc_id]["balance"] -= data.amount

    return {
        "message": "Withdrawal successful",
        "account_id": acc_id,
        "new_balance": accounts[acc_id]["balance"]
    }


# -----------------------------
# Transfer
# -----------------------------
@app.post("/transfer")
def transfer(data: TransferModel):

    if data.from_acc not in accounts:
        return {"error": "Sender account not found"}

    if data.to_acc not in accounts:
        return {"error": "Receiver account not found"}

    if accounts[data.from_acc]["balance"] < data.amount:
        return {"error": "Insufficient balance"}

    # Transfer money
    accounts[data.from_acc]["balance"] -= data.amount
    accounts[data.to_acc]["balance"] += data.amount

    return {
        "message": "Transfer successful",
        "from_account": data.from_acc,
        "from_balance": accounts[data.from_acc]["balance"],
        "to_account": data.to_acc,
        "to_balance": accounts[data.to_acc]["balance"]
    }


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8080, reload=True)