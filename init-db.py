#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""
import os
import sys

# Добавляем путь к приложению
sys.path.insert(0, '/app')

from app import app, db

def init_database():
    """Создает базу данных и все таблицы"""
    try:
        with app.app_context():
            # Создаем все таблицы
            db.create_all()
            print("✅ База данных успешно создана!")
            
            # Создаем администратора по умолчанию
            from models.user import User
            from werkzeug.security import generate_password_hash
            
            # Проверяем, есть ли уже админ
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
        print(f"❌ Ошибка при создании базы данных: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_database()
