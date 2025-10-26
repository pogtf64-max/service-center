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

def fix_user_model():
    """Исправить модель User"""
    print("🔧 Исправляю модель User...")
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    
    # Проверим содержимое models/user.py
    print("📋 Проверяю models/user.py...")
    user_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && cat models/user.py'")
    print(f"Содержимое models/user.py:\n{user_content.stdout}")
    
    # Создадим правильную модель User без can_manage_settings
    correct_user = '''from models.database import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'
'''
    
    # Создадим правильный файл на сервере
    print("📝 Создаю правильную модель User на сервере...")
    create_cmd = f"cat > /tmp/user_correct.py << 'EOF'\n{correct_user}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/user_correct.py service-center-service-center-1:/app/models/user.py")
        
        if copy_result.returncode == 0:
            print("✅ Модель User исправлена на сервере!")
            
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
    fix_user_model()
