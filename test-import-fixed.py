#!/usr/bin/env python3
"""
Тест импорта модулей (исправленная версия)
"""
import sys
print("Python path:", sys.path)

try:
    print("Импортируем routes...")
    from routes import register_blueprints
    print("✅ routes импортирован успешно!")
    
    print("Импортируем app...")
    from app import create_app
    print("✅ create_app импортирован успешно!")
    
    print("Создаем приложение...")
    app = create_app()
    print("✅ Приложение создано успешно!")
    
    print("Все импорты работают!")
    
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
