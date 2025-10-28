#!/usr/bin/env python3
"""
Простой тест приложения
"""
import os
import sys

# Добавляем путь к приложению
sys.path.insert(0, '/app')

try:
    print("Импортируем app...")
    from app import app
    print("✅ App импортирован успешно!")
    
    print("Проверяем конфигурацию...")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY', 'НЕ УСТАНОВЛЕН')}")
    print(f"DATABASE_URI: {app.config.get('DATABASE_URI', 'НЕ УСТАНОВЛЕН')}")
    
    print("Проверяем базу данных...")
    with app.app_context():
        from app import db
        print("✅ База данных подключена!")
        
        # Пробуем создать таблицы
        db.create_all()
        print("✅ Таблицы созданы!")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
