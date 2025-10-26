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

def fix_stopped_container():
    """Исправить файл в остановленном контейнере"""
    print("🔧 Исправляю app.py в остановленном контейнере...")
    
    # Создадим правильный app.py
    correct_app = '''from flask import Flask
from flask_login import LoginManager
from models.database import db
from models.user import User
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.clients import clients_bp
from routes.orders import orders_bp
from routes.parts import parts_bp
from routes.devices import devices_bp
from routes.archive import archive_bp
from routes.services import services

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_center.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрируем blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(clients_bp, url_prefix="/clients")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(parts_bp, url_prefix="/parts")
app.register_blueprint(devices_bp, url_prefix="/devices")
app.register_blueprint(archive_bp, url_prefix="/archive")
app.register_blueprint(services, url_prefix="/services")

@app.route('/')
def index():
    from flask import redirect, url_for
    return redirect(url_for('dashboard.index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
'''
    
    # Запишем исправленный app.py через временный файл
    print("📝 Создаю временный файл...")
    temp_file = "/tmp/app_fixed.py"
    
    # Создадим файл на сервере
    create_cmd = f"cat > {temp_file} << 'EOF'\n{correct_app}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        print("✅ Временный файл создан!")
        
        # Скопируем файл в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_cmd = f"docker cp {temp_file} service-center-service-center-1:/app/app.py"
        copy_result = run_ssh_command(copy_cmd)
        
        if copy_result.returncode == 0:
            print("✅ Файл скопирован в контейнер!")
            
            # Проверим синтаксис
            print("🔍 Проверяю синтаксис...")
            syntax_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -m py_compile app.py'")
            
            if syntax_check.returncode == 0:
                print("✅ Синтаксис корректен!")
                
                # Запустим контейнер
                print("🚀 Запускаю контейнер...")
                start_result = run_ssh_command("docker start service-center-service-center-1")
                
                if start_result.returncode == 0:
                    print("✅ Контейнер запущен!")
                    
                    # Подождем и проверим
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
                        print("❌ Flask приложение не запустилось")
                else:
                    print(f"❌ Ошибка запуска: {start_result.stderr}")
            else:
                print(f"❌ Синтаксическая ошибка: {syntax_check.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания файла: {create_result.stderr}")

if __name__ == "__main__":
    fix_stopped_container()
