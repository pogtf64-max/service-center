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

def fix_app_py():
    """Исправить app.py на сервере"""
    print("🔧 Исправляю app.py на сервере...")
    
    # Проверим app.py
    result = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && grep -n services app.py'")
    print(f"Проверка services: {result.stdout}")
    
    if "services" not in result.stdout:
        print("❌ services не найден в app.py, добавляю...")
        
        # Добавим импорт services
        add_import = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && sed -i \"/from routes.dashboard import dashboard_bp/a from routes.services import services\" app.py'")
        
        # Добавим регистрацию services
        add_register = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && sed -i \"/app.register_blueprint(dashboard_bp, url_prefix=\\\"/dashboard\\\")/a app.register_blueprint(services, url_prefix=\\\"/services\\\")\" app.py'")
        
        print("✅ services добавлен в app.py")
    else:
        print("✅ services уже есть в app.py")
    
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

if __name__ == "__main__":
    fix_app_py()
