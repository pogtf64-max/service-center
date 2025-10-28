#!/usr/bin/env python3
"""
Скрипт для инициализации полной базы данных
"""
import os
import sys

# Добавляем путь к приложению
sys.path.insert(0, '/app')

try:
    from app import app, db
    
    print("Инициализация полной базы данных...")
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        print("✅ Все таблицы созданы!")
        
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
            
        # Создаем тестовые данные
        from models.service import Service
        from models.client import Client
        from models.device import Device
        
        # Проверяем, есть ли уже данные
        if Service.query.count() == 0:
            # Создаем тестовые услуги
            services = [
                Service(name="Диагностика", price=1000, description="Полная диагностика устройства"),
                Service(name="Замена экрана", price=5000, description="Замена поврежденного экрана"),
                Service(name="Ремонт кнопок", price=2000, description="Ремонт неработающих кнопок"),
                Service(name="Чистка от пыли", price=1500, description="Чистка устройства от пыли и грязи")
            ]
            
            for service in services:
                db.session.add(service)
            
            # Создаем тестового клиента
            client = Client(
                name="Иван Петров",
                phone="+7 (999) 123-45-67",
                email="ivan@example.com"
            )
            db.session.add(client)
            
            # Создаем тестовое устройство
            device = Device(
                brand="Samsung",
                model="Galaxy S21",
                serial_number="SN123456789",
                client_id=1
            )
            db.session.add(device)
            
            db.session.commit()
            print("✅ Тестовые данные созданы!")
        else:
            print("ℹ️ Тестовые данные уже существуют")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
