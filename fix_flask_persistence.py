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

def fix_flask_persistence():
    """Исправить постоянство Flask"""
    print("🔧 ИСПРАВЛЯЮ ПОСТОЯНСТВО FLASK")
    print("=" * 40)
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    run_ssh_command("docker stop service-center-service-center-1")
    
    # Создадим исправленный app.py с правильным запуском
    fixed_app = '''from flask import Flask, redirect, url_for
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
from routes.devtools import devtools_bp

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
app.register_blueprint(devtools_bp, url_prefix="/devtools")

@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))

# ДОБАВЛЯЕМ ПРЯМОЙ МАРШРУТ /dashboard
@app.route('/dashboard')
def dashboard_redirect():
    return redirect(url_for('dashboard.index'))

if __name__ == '__main__':
    print("🚀 Запуск Flask приложения...")
    with app.app_context():
        db.create_all()
        print("✅ База данных инициализирована")
    
    print("🌐 Flask запущен на http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
'''
    
    # Создадим исправленный файл
    print("📝 Создаю исправленный app.py...")
    create_cmd = f"cat > /tmp/app_persistent.py << 'EOF'\n{fixed_app}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/app_persistent.py service-center-service-center-1:/app/app.py")
        
        if copy_result.returncode == 0:
            print("✅ app.py исправлен!")
            
            # Запустим контейнер
            print("🚀 Запускаю контейнер...")
            start_result = run_ssh_command("docker start service-center-service-center-1")
            
            if start_result.returncode == 0:
                print("✅ Контейнер запущен!")
                
                # Подождем
                import time
                time.sleep(5)
                
                # Проверим логи
                print("🔍 Проверяю логи...")
                logs = run_ssh_command("docker logs service-center-service-center-1 --tail 20")
                print(f"Логи: {logs.stdout}")
                
                # Проверим процессы
                print("🔍 Проверяю процессы...")
                processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux | grep python'")
                print(f"Процессы: {processes.stdout}")
                
                # Проверим доступность
                print("🔍 Проверяю доступность...")
                access_test = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/")
                print(f"Доступность: {access_test.stdout}")
                
                if "🚀 Запуск Flask приложения" in logs.stdout:
                    print("🎉 FLASK ЗАПУЩЕН ПОСТОЯННО!")
                    print("🌐 Проверьте https://miservis27.ru/")
                else:
                    print("❌ Flask все еще не запускается постоянно")
            else:
                print(f"❌ Ошибка запуска: {start_result.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания файла: {create_result.stderr}")

if __name__ == "__main__":
    fix_flask_persistence()
