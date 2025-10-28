#!/usr/bin/env python3
"""
Тест импорта модулей
"""
import sys
print("Python path:", sys.path)

try:
    print("Импортируем routes...")
    from routes import register_blueprints
    print("✅ routes импортирован успешно!")
    
    print("Импортируем app...")
    from app import app
    print("✅ app импортирован успешно!")
    
    print("Все импорты работают!")
    
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
