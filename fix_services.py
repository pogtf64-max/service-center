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

def fix_services_blueprint():
    """Исправить регистрацию services blueprint"""
    print("🔧 Исправляю services blueprint...")
    
    # Проверим текущий app.py
    app_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && cat app.py'")
    print(f"Текущий app.py:\n{app_content.stdout}")
    
    # Создадим исправленный app.py
    fixed_app = '''from flask import Flask
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
    return redirect(url_for('dashboard.index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
'''
    
    # Запишем исправленный app.py
    write_cmd = f"docker exec -i service-center-service-center-1 bash -c 'cd /app && cat > app.py << \"EOF\"\n{fixed_app}\nEOF'"
    result = run_ssh_command(write_cmd)
    
    if result.returncode == 0:
        print("✅ app.py исправлен!")
        
        # Перезапустим контейнер
        print("🔄 Перезапускаю контейнер...")
        restart = run_ssh_command("docker restart service-center-service-center-1")
        
        if restart.returncode == 0:
            print("✅ Контейнер перезапущен!")
            
            # Проверим логи
            print("📋 Проверяю логи...")
            logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
            print(f"Логи: {logs.stdout}")
            
            if "error" not in logs.stdout.lower():
                print("🎉 Проблема исправлена! Сервер работает!")
            else:
                print("❌ Есть ошибки в логах")
        else:
            print(f"❌ Ошибка перезапуска: {restart.stderr}")
    else:
        print(f"❌ Ошибка записи app.py: {result.stderr}")

if __name__ == "__main__":
    fix_services_blueprint()
