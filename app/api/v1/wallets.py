from typing import Optional

from app.service import wallets as wallet_service
from fastapi import APIRouter, Depends

from app.shemas import CreateWalletRequest
from sqlalchemy.orm import Session

from app.dependency import get_db

router = APIRouter()

@router.get('/balance')
def get_balance(wallet_name: Optional[str] = None, db: Session = Depends(get_db)):
    return wallet_service.get_balance(db, wallet_name)


@router.post('/wallets')
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db)):
    return wallet_service.create_wallet(db, wallet)

