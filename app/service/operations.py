from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import User
from ..shemas import OperationsRequest
from ..repository import wallets as wallet_repository


def add_income(db: Session, current_user: User, operation: OperationsRequest):
    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, operation.wallet_name, current_user.id):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Добавляем сумму к балансу кошелька
    wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount, current_user.id)
    db.commit()
    # Возвращаем иформацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }

def add_expense(db: Session, current_user: User, operation: OperationsRequest):
    #   Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, operation.wallet_name, current_user.id):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    #   Проверяем, что на кошельке достаточно средств
    wallet = wallet_repository.get_wallet_balance_by_name(db, operation.wallet_name, current_user.id)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Not enough funds in wallet {wallet.balance}'
        )
    #   Вычитаем расход из баланса кошелька
    wallet = wallet_repository.add_expense(db, operation.wallet_name, operation.amount, current_user.id)
    db.commit()
    #   Возвращаем информацию об операции
    return {
        "message": f"Wallet {operation.wallet_name} expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }
