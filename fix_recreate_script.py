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

def fix_recreate_script():
    """Исправить скрипт пересоздания БД"""
    print("🔧 Исправляю скрипт пересоздания БД...")
    
    # Создадим правильный скрипт
    correct_script = '''from flask import Flask
from models.database import db
from models.user import User
from models.service import Service
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_center.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Удаляем все таблицы
    db.drop_all()
    
    # Создаем все таблицы заново
    db.create_all()
    
    # Создаем администратора
    admin = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        role='admin',
        full_name='Системный администратор',
        is_active=True,
        is_approved=True
    )
    db.session.add(admin)
    db.session.flush()
    
    # Создаем сервис по умолчанию
    default_service = Service(
        name='Административная панель',
        address='Системный сервис',
        service_password=generate_password_hash('admin123'),
        director_id=admin.id
    )
    db.session.add(default_service)
    db.session.flush()
    
    # Обновляем service_id у администратора
    admin.service_id = default_service.id
    
    db.session.commit()
    print("База данных пересоздана!")
'''
    
    # Создадим правильный скрипт на сервере
    print("📝 Создаю правильный скрипт...")
    create_cmd = f"cat > /tmp/recreate_db_fixed.py << 'EOF'\n{correct_script}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем скрипт в контейнер
        print("📋 Копирую скрипт в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/recreate_db_fixed.py service-center-service-center-1:/app/recreate_db.py")
        
        if copy_result.returncode == 0:
            # Запустим скрипт
            print("🚀 Запускаю исправленный скрипт...")
            run_script = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python recreate_db.py'")
            print(f"Результат: {run_script.stdout}")
            
            if run_script.stderr:
                print(f"Ошибки: {run_script.stderr}")
            
            if run_script.returncode == 0:
                print("✅ База данных пересоздана!")
                
                # Перезапустим контейнер
                print("🔄 Перезапускаю контейнер...")
                restart_result = run_ssh_command("docker restart service-center-service-center-1")
                
                if restart_result.returncode == 0:
                    print("✅ Контейнер перезапущен!")
                    
                    # Подождем
                    import time
                    time.sleep(5)
                    
                    # Проверим логи
                    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
                    print(f"Логи: {logs.stdout}")
                    
                    if "Running on" in logs.stdout:
                        print("🎉 Flask приложение запущено! База данных исправлена!")
                        print("🌐 Проверьте https://miservis27.ru/dashboard")
                    else:
                        print("❌ Flask приложение все еще не запускается")
                else:
                    print(f"❌ Ошибка перезапуска: {restart_result.stderr}")
            else:
                print(f"❌ Ошибка выполнения скрипта: {run_script.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания скрипта: {create_result.stderr}")

if __name__ == "__main__":
    fix_recreate_script()
