import os
from pathlib import Path
from sqlalchemy import text
from app.database import engine, Base

print("🗑️  Удаление всех данных из БД...")

try:
    # Удаляем все таблицы из основной БД PostgreSQL
    with engine.connect() as connection:
        # Отключаем ограничения внешних ключей
        connection.execute(text("DROP TABLE IF EXISTS wallet CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS \"user\" CASCADE"))
        connection.commit()
    print("✅ Таблицы удалены из PostgreSQL")
except Exception as e:
    print(f"⚠️  Ошибка при удалении таблиц: {e}")

# Удаляем тестовую БД SQLite если существует
# test_db_path = Path("test.db")
# if test_db_path.exists():
#     try:
#         test_db_path.unlink()
#         print("✅ Тестовая БД test.db удалена")
#     except Exception as e:
#         print(f"⚠️  Ошибка при удалении test.db: {e}")

# Пересоздаем таблицы
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы пересоздана с актуальной схемой")
except Exception as e:
    print(f"❌ Ошибка при создании таблиц: {e}")

print("\n🎉 База данных успешно очищена и обновлена!")

