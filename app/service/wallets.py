from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..shemas import CreateWalletRequest
from ..repository import wallets as wallet_repository


def get_balance(db: Session, wallet_name: Optional[str] = None):
    # Если имя не указано - считаем общий баланс
    if wallet_name is None:
        wallets = wallet_repository.get_all_wallets(db)
        return {'total balance': sum([w.balance for w in wallets])}

    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(db, wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet_name} not found"
        )

    # Возвращаем баланс конкретного кошелька
    wallet = wallet_repository.get_wallet_balance_by_name(db, wallet_name)
    return {'wallet': wallet.name, 'balance': wallet.balance}

def create_wallet(db: Session, wallet: CreateWalletRequest):
    # Проверяем есть ли такой кошелек
    if wallet_repository.is_wallet_exist(db, wallet.name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet.name} already exists"
        )
    # Создаем Новый кошелек с начальным балансом
    wallet = wallet_repository.create_wallet(db, wallet.name, wallet.initial_balance)
    db.commit()
    # Возвращаем информацию о созднанном кошельке
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": wallet.balance
    }
