#!/usr/bin/env python3
"""
Скрипт для создания базы данных
"""
import os
import sys

# Добавляем путь к приложению
sys.path.insert(0, '/app')

try:
    from app import app, db
    
    print("Создаем базу данных...")
    with app.app_context():
        db.create_all()
        print("✅ База данных создана успешно!")
        
        # Создаем администратора
        from models.user import User
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@service-center.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                can_manage_settings=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Администратор создан: admin / admin123")
        else:
            print("ℹ️ Администратор уже существует")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
