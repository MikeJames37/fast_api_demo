from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


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
    model_config = {"from_attributes": True}

    id: int
