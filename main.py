import operator

from fastapi import FastAPI, HTTPException
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError

app = FastAPI()

BALANCE = {}


class OperationsRequest(BaseModel):
    wallet_name: str = Field(..., max_length=100)
    amount: float
    description: Optional[str] = Field(None, max_length=255)

    # Валидация суммы - она должна быть положительной
    @field_validator('amount')
    def amount_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Amount must be greater than zero')
        return value

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Wallet name cannot be empty')
        return value

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=100)
    initial_balance: float = 0

    @field_validator('name')
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Wallet name cannot be empty')
        return value

    @field_validator('initial_balance')
    def balance_not_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError('Initial balance cannot be negative')
        return value


@app.get('/balance')
def get_balance(wallet_name: Optional[str] = None):
    # Если имя не указано - считаем общий баланс
    if wallet_name is None:
        return {'total balance': sum(BALANCE.values())}

    # Проверяем существует ли кошелек
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet_name} not found"
        )

    # Возвращаем баланс конкретного кошелька
    return {'wallet': wallet_name, 'balance': BALANCE[wallet_name]}


@app.post('/wallets')
def create_wallet(wallet: CreateWalletRequest):
    # Проверяем есть ли такой кошелек
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet.name} already exists"
        )
    # Создаем Новый кошелек с начальным балансом
    BALANCE[wallet.name] = wallet.initial_balance

    # Возвращаем информацию о созднанном кошельке
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": BALANCE[wallet.name]
    }


@app.post("/operations/income")
def add_income(operation: OperationsRequest):
    # Проверяем существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Добавляем сумму к балансу кошелька
    BALANCE[operation.wallet_name] += operation.amount

    # Возвращаем иформацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': BALANCE[operation.wallet_name]
    }

@app.post("/operations/expense")
def add_expense(operation: OperationsRequest):
    #   Проверяем существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    #   Проверяем, что на кошельке достаточно средств
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Not enough funds in wallet {BALANCE[operation.wallet_name]}'
        )
    #   Вычитаем расход из баланса кошелька
    BALANCE[operation.wallet_name] -= operation.amount
    #   Возвращаем информацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': BALANCE[operation.wallet_name]
    }
