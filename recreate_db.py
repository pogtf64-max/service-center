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

def recreate_database():
    """Пересоздать базу данных"""
    print("🔧 Пересоздаю базу данных...")
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    
    # Удалим старую базу данных
    print("🗑️ Удаляю старую базу данных...")
    rm_db = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'rm -f /app/instance/service_center.db'")
    print(f"Удаление БД: {rm_db.stdout}")
    
    # Создадим скрипт для пересоздания БД
    recreate_script = '''from app import app
from models.database import db
from models.user import User
from models.service import Service
from werkzeug.security import generate_password_hash

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
    
    # Создадим скрипт на сервере
    print("📝 Создаю скрипт пересоздания БД...")
    create_cmd = f"cat > /tmp/recreate_db.py << 'EOF'\n{recreate_script}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем скрипт в контейнер
        print("📋 Копирую скрипт в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/recreate_db.py service-center-service-center-1:/app/recreate_db.py")
        
        if copy_result.returncode == 0:
            # Запустим скрипт
            print("🚀 Запускаю скрипт пересоздания БД...")
            run_script = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python recreate_db.py'")
            print(f"Результат: {run_script.stdout}")
            
            if run_script.returncode == 0:
                print("✅ База данных пересоздана!")
                
                # Запустим контейнер
                print("🚀 Запускаю контейнер...")
                start_result = run_ssh_command("docker start service-center-service-center-1")
                
                if start_result.returncode == 0:
                    print("✅ Контейнер запущен!")
                    
                    # Подождем
                    import time
                    time.sleep(5)
                    
                    # Проверим логи
                    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
                    print(f"Логи: {logs.stdout}")
                    
                    if "Running on" in logs.stdout:
                        print("🎉 Flask приложение запущено! База данных исправлена!")
                    else:
                        print("❌ Flask приложение все еще не запускается")
                else:
                    print(f"❌ Ошибка запуска: {start_result.stderr}")
            else:
                print(f"❌ Ошибка выполнения скрипта: {run_script.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания скрипта: {create_result.stderr}")

if __name__ == "__main__":
    recreate_database()
