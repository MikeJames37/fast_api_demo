from enum import Enum, auto


class CurrencyEnum(str, Enum):
    RUB = "rub"
    USD = "usd"
    EUR = "eur"

class OperationType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"
