from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.enum import CurrencyEnum
from app.models import Wallet, User


# BALANCE: dict[str:float] = {}

def is_wallet_exist(db: Session, wallet_name:str, user_id:int = None) -> bool:
    #Проверяем существует ли кошелек
    query = db.query(Wallet).filter(Wallet.name == wallet_name)
    if user_id is not None:
        query = query.filter(Wallet.user_id == user_id)
    return query.first() is not None


def add_income(db: Session, wallet_name:str, amount:Decimal, user_id:int) -> Optional[Wallet]:
    #Добавляем доход к балансу кошелька
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance += amount
    return wallet

    #   Возвращаем новый баланс кошелька


def get_wallet_balance_by_name(db: Session, wallet_name:str, user_id:int) -> Optional[Wallet]:
    #   Возвращаем баланс кошелька по его названию
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()

def add_expense(db: Session, wallet_name:str, amount:Decimal, user_id:int) -> Optional[Wallet]:
    #   Вычитаем расход из баланса кошелька
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance -= amount
    return wallet

def get_all_wallets(db: Session, user_id:int) -> list[Wallet]:
    #   Возвращаем все кошельки пользователя
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()

def create_wallet(db: Session, user_id:int, wallet_name:str, amount:Decimal, currency: CurrencyEnum) -> Wallet:
    #   Создаем новый кошелек с указанным балансом
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id, currency=currency)
    db.add(wallet)
    db.flush()
    return wallet

def get_wallet_by_id(db: Session, user_id: int, wallet_id:int) -> Optional[Wallet]:
    return db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user_id).scalar()
