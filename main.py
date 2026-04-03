import operator

from fastapi import FastAPI, HTTPException
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError

from app.database import Base, engine
from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

#Создаем экземпляр приложения FastAPI
app = FastAPI()

#Подключаем роутер для работы с кошельками с префиксом /api/v1
app.include_router(wallets_router, prefix="/api/v1", tags=["wallets"])
#   Подключаем роутер для работы с операциями с префиксом /api/v1
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])

app.include_router(users_router, prefix="/api/v1", tags=["users"])

#   Создаем все таблицы в базе данных, при старте приложения
Base.metadata.create_all(bind=engine)


