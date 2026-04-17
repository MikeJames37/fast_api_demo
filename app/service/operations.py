from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .exchange_service import get_exchange_rate
from ..database import SessionLocal
from ..enum import OperationType
from ..models import User
from ..shemas import OperationsRequest, OperationResponse
from ..repository import wallets as wallet_repository
from ..repository import operations as operations_repository


def add_income(db: Session, current_user: User, operation: OperationsRequest) -> OperationResponse:
    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, operation.wallet_name, current_user.id):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Добавляем сумму к балансу кошелька
    wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount, current_user.id)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type= OperationType.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
    )
    db.commit()
    # Возвращаем иформацию об операции
    return OperationResponse.model_validate(operation)

def add_expense(db: Session, current_user: User, operation: OperationsRequest) -> OperationResponse:
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
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type= OperationType.EXPENSE,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
    )
    db.commit()
    #   Возвращаем информацию об операции
    return OperationResponse.model_validate(operation)

def get_operations_list(
        db: Session,
        current_user: User,
        wallet_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
) -> list[OperationResponse]:

    if wallet_id:
        wallet = wallet_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet {wallet_id} not found"
            )
        wallets_ids = [wallet.id]
    else:
       wallets = wallet_repository.get_all_wallets(db, current_user.id)
       wallets_ids = [w.id for w in wallets]

    operations = operations_repository.get_operations_list(db, wallets_ids, date_from, date_to)

    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
    return result

async def transfer_between_wallets(
        db: Session, user_id: int, from_wallet_id: int, to_wallet_id: int, amount: Decimal,
) -> OperationResponse:
    from_wallet = wallet_repository.get_wallet_by_id(db, user_id, from_wallet_id)
    to_wallet = wallet_repository.get_wallet_by_id(db, user_id, to_wallet_id)

    if not from_wallet or not to_wallet:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {from_wallet_id} or {to_wallet_id} not found"
        )

    if from_wallet.balance < amount:
        raise HTTPException(
            status_code=400,
            detail=f'Not enough money in wallet {from_wallet.balance} {from_wallet.currency}'
        )

    target_amount = amount
    exchange_rate = 1.0
    if from_wallet.currency != to_wallet.currency:
        exchange_rate = await get_exchange_rate(
            from_wallet.currency,
            to_wallet.currency,
        )
        target_amount = round(amount * exchange_rate, 2) #Конвертируем сумму

    from_wallet.balance = round(from_wallet.balance - amount, 2) #Списываем
    to_wallet.balance = round(to_wallet.balance + target_amount, 2) #Зачисляем
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=from_wallet.id,
        type= OperationType.TRANSFER,
        amount=target_amount,
        currency=to_wallet.currency,
        category='перевод',
    )
    db.add(from_wallet)
    db.add(to_wallet)
    db.add(operation)
    db.commit()
    return OperationResponse.model_validate(operation)
        
