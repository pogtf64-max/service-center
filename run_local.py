#!/usr/bin/env python3
"""
Локальный запуск приложения для разработки
"""
from app import create_app
import os

if __name__ == '__main__':
    # Создаем приложение
    app = create_app()
    
    # Настройки для локальной разработки
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'local-development-secret-key'
    
    # Создаем директорию instance если её нет
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    print("Запуск локального сервера разработки...")
    print("Приложение будет доступно по адресу: http://localhost:5000")
    print("Режим отладки включен")
    print("Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    # Запуск на локальном порту
    app.run(host='0.0.0.0', port=5000, debug=True)
