#!/usr/bin/env python3
"""
Скрипт для исправления проблемы с UNIQUE constraint на email
"""
from app import create_app
from models.database import db
from models.user import User

def fix_email_constraint():
    app = create_app()
    with app.app_context():
        try:
            # Найти пользователей с пустым email
            users_with_empty_email = User.query.filter_by(email='').all()
            print(f'Найдено пользователей с пустым email: {len(users_with_empty_email)}')
            
            # Установить None вместо пустой строки для email
            for user in users_with_empty_email:
                print(f'Обновляем пользователя: {user.username} (ID: {user.id})')
                user.email = None
            
            # Сохранить изменения
            db.session.commit()
            print('База данных успешно обновлена')
            
            # Проверить результат
            remaining_empty = User.query.filter_by(email='').count()
            print(f'Осталось пользователей с пустым email: {remaining_empty}')
            
        except Exception as e:
            print(f'Ошибка при обновлении базы данных: {e}')
            db.session.rollback()

if __name__ == '__main__':
    fix_email_constraint()
