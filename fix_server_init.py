#!/usr/bin/env python3
import subprocess
import os

def run_ssh_command(command):
    """Выполнить SSH команду"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    cmd = ["ssh", "-i", ssh_key, ssh_host, command]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result

def fix_server_init():
    """Исправить routes/__init__.py на сервере"""
    print("🔧 Исправляю routes/__init__.py на сервере...")
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    
    # Создадим правильный routes/__init__.py на сервере
    correct_init = '''from flask import Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .clients import clients_bp
from .orders import orders_bp
from .parts import parts_bp
from .devices import devices_bp
from .archive import archive_bp
from .services import services
from .devtools import devtools_bp

def register_blueprints(app):
    """Регистрация всех blueprints"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(parts_bp, url_prefix="/parts")
    app.register_blueprint(devices_bp, url_prefix="/devices")
    app.register_blueprint(archive_bp, url_prefix="/archive")
    app.register_blueprint(services, url_prefix="/services")
    app.register_blueprint(devtools_bp, url_prefix="/devtools")
'''
    
    # Создадим файл на сервере
    print("📝 Создаю правильный routes/__init__.py на сервере...")
    create_cmd = f"cat > /tmp/__init__.py << 'EOF'\n{correct_init}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/__init__.py service-center-service-center-1:/app/routes/__init__.py")
        
        if copy_result.returncode == 0:
            print("✅ Файл исправлен на сервере!")
            
            # Запустим контейнер
            print("🚀 Запускаю контейнер...")
            start_result = run_ssh_command("docker start service-center-service-center-1")
            
            if start_result.returncode == 0:
                print("✅ Контейнер запущен!")
                
                # Подождем
                import time
                time.sleep(5)
                
                # Проверим статус
                status = run_ssh_command("docker ps | grep service-center-service-center-1")
                print(f"Статус: {status.stdout}")
                
                # Проверим логи
                logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
                print(f"Логи: {logs.stdout}")
                
                if "Running on" in logs.stdout:
                    print("🎉 Flask приложение запущено! Ошибка 502 исправлена!")
                else:
                    print("❌ Flask приложение все еще не запускается")
            else:
                print(f"❌ Ошибка запуска: {start_result.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания файла: {create_result.stderr}")

if __name__ == "__main__":
    fix_server_init()
