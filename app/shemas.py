from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.enum import CurrencyEnum


class OperationsRequest(BaseModel):
    wallet_name: str = Field(..., max_length=100)
    amount: Decimal
    description: Optional[str] = Field(None, max_length=255)

    # Валидация суммы - она должна быть положительной
    @field_validator('amount')
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError('Amount must be greater than zero')
        return value

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Wallet name cannot be empty')
        return value


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=100)
    initial_balance: Decimal = 0

    currency: CurrencyEnum = CurrencyEnum.RUB

    @field_validator('name')
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Wallet name cannot be empty')
        return value

    @field_validator('initial_balance')
    def balance_not_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError('Initial balance cannot be negative')
        return value

class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)

class UserResponse(UserRequest):
    #   Настройка для автоматического создания моделей из атрибутов Объекта
    model_config = {"from_attributes": True}
    id: int

class WalletResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum

class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: Optional[str]
    subcategory: Optional[str]
    created_at: datetime

class TransferCreateShema(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    amount: Decimal

    @field_validator('to_wallet_id')
    @classmethod
    def wallets_must_differ(
            cls, v: int, info) -> int:
        if'from_wallet_id' in info.data and v == info.data['from_wallet_id']:
            raise ValueError('Same wallets ids!')
        return v

    @field_validator('amount')
    @classmethod
    def amount_gt_zero(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError('Amount cannot be negative')
        return v