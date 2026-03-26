from typing import Optional

from fastapi import HTTPException

from ..shemas import CreateWalletRequest
from ..repository import wallets as wallet_repository


def get_balance(wallet_name: Optional[str] = None):
    # Если имя не указано - считаем общий баланс
    if wallet_name is None:
        wallets = wallet_repository.get_all_wallets()
        return {'total balance': sum(wallets.values())}

    # Проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet_name} not found"
        )

    # Возвращаем баланс конкретного кошелька
    balance = wallet_repository.get_wallet_balance_by_name(wallet_name)
    return {'wallet': wallet_name, 'balance': balance}


def create_wallet(wallet: CreateWalletRequest):
    # Проверяем есть ли такой кошелек
    if wallet_repository.is_wallet_exist(wallet.name):
        raise HTTPException(
            status_code=409,
            detail=f"Wallet {wallet.name} already exists"
        )
    # Создаем Новый кошелек с начальным балансом
    new_balance = wallet_repository.create_wallet(wallet.name, wallet.initial_balance)
    # Возвращаем информацию о созднанном кошельке
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": new_balance
    }
