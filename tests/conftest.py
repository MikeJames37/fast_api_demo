import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.testclient import TestClient

from app.database import Base
from app.dependency import get_db
from main import app

# Загружаем переменные из .env файла
load_dotenv()

# Получаем значения из переменных окружения
DB_USER = os.getenv("DB_USER", "postgres")  # postgres - значение по умолчанию
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "finance_db")

# DATABASE_URL = "sqlite:///./finance.db"
TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/test_db"
test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Base = declarative_base()

def get_test_db() -> Generator[Session, None, None]:
    #   Создаем новую сессию для работы с базой данных тестов
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Пересоздаем все таблицы перед тестом
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db_session()-> Generator[Session, None, None]:
    #   Создаем новую сессию для работы с базой данных тестов
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

