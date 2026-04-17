from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..enum import CurrencyEnum
from ..models import User
from ..shemas import CreateWalletRequest, WalletResponse, TotalBalance
from ..repository import wallets as wallet_repository
from app.service import exchange_service


async def get_total_balance(db: Session, current_user: User) -> TotalBalance:
    # Если имя не указано - считаем общий баланс

    wallets = wallet_repository.get_all_wallets(db, current_user.id)
    total_balance = Decimal(0)
    for wallet in wallets:
        if wallet.currency == CurrencyEnum.RUB:
            total_balance += wallet.balance
        else:
            exchange_rate = await exchange_service.get_exchange_rate(wallet.currency, CurrencyEnum.RUB)
            total_balance += exchange_rate * wallet.balance
    return TotalBalance(total_balance=total_balance)



def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest) -> WalletResponse:
    # Проверяем есть ли такой кошелек
    if wallet_repository.is_wallet_exist(db, wallet.name, current_user.id):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet.name} already exists"
        )
    # Создаем Новый кошелек с начальным балансом
    wallet = wallet_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    db.commit()
    # Возвращаем информацию о созднанном кошельке
    return WalletResponse.model_validate(wallet)

def get_all_wallets(db: Session, current_user: User) -> list[WalletResponse]:
    wallets = wallet_repository.get_all_wallets(db, current_user.id)
    return [WalletResponse.model_validate(wallet) for wallet in wallets]