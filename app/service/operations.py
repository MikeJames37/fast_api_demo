from fastapi import HTTPException

from ..shemas import OperationsRequest
from ..repository import wallets as wallet_repository


def add_income(operation: OperationsRequest):
    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Добавляем сумму к балансу кошелька
    new_balance = wallet_repository.add_income(operation.wallet_name, operation.amount)

    # Возвращаем иформацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': new_balance
    }

def add_expense(operation: OperationsRequest):
    #   Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    #   Проверяем, что на кошельке достаточно средств
    balance = wallet_repository.get_wallet_balance_by_name(operation.wallet_name)
    if balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Not enough funds in wallet {balance}'
        )
    #   Вычитаем расход из баланса кошелька
    new_balance = wallet_repository.add_expense(operation.wallet_name, operation.amount)
    #   Возвращаем информацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': new_balance
    }