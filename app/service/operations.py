from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..shemas import OperationsRequest
from ..repository import wallets as wallet_repository


def add_income(db: Session, operation: OperationsRequest):
    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Добавляем сумму к балансу кошелька
    wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount)
    db.commit()
    # Возвращаем иформацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }

def add_expense(db: Session, operation: OperationsRequest):
    #   Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    #   Проверяем, что на кошельке достаточно средств
    wallet = wallet_repository.get_wallet_balance_by_name(db, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Not enough funds in wallet {wallet.balance}'
        )
    #   Вычитаем расход из баланса кошелька
    wallet = wallet_repository.add_expense(db, operation.wallet_name, operation.amount)
    db.commit()
    #   Возвращаем информацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }
