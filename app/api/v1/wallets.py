from typing import Optional

from app.service import wallets as wallet_service
from fastapi import APIRouter

from app.shemas import CreateWalletRequest

router = APIRouter()

@router.get('/balance')
def get_balance(wallet_name: Optional[str] = None):
    return wallet_service.get_balance(wallet_name)


@router.post('/wallets')
def create_wallet(wallet: CreateWalletRequest):
    return wallet_service.create_wallet(wallet)

