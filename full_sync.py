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

def upload_file(local_path, server_path):
    """Загрузить файл на сервер"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    # Читаем локальный файл
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения {local_path}: {e}")
        return False
    
    # Создаем временный файл
    temp_file = f"/tmp/{os.path.basename(local_path)}"
    
    # Загружаем файл на сервер
    scp_cmd = ["scp", "-i", ssh_key, local_path, f"{ssh_host}:{temp_file}"]
    scp_result = subprocess.run(scp_cmd, capture_output=True, text=True, encoding='utf-8')
    
    if scp_result.returncode == 0:
        # Копируем файл в контейнер
        copy_cmd = ["ssh", "-i", ssh_key, ssh_host, f"docker cp {temp_file} service-center-service-center-1:{server_path}"]
        copy_result = subprocess.run(copy_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if copy_result.returncode == 0:
            print(f"✅ {local_path} → {server_path}")
            return True
        else:
            print(f"❌ Ошибка копирования {local_path}: {copy_result.stderr}")
            return False
    else:
        print(f"❌ Ошибка загрузки {local_path}: {scp_result.stderr}")
        return False

def full_sync():
    """Полная синхронизация проекта"""
    print("🚀 Начинаю полную синхронизацию проекта...")
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    print(f"Остановка: {stop_result.stdout}")
    
    # Список всех файлов для синхронизации
    files_to_sync = [
        # Основные файлы
        ("app.py", "/app/app.py"),
        ("config.py", "/app/config.py"),
        ("requirements.txt", "/app/requirements.txt"),
        
        # Models
        ("models/__init__.py", "/app/models/__init__.py"),
        ("models/database.py", "/app/models/database.py"),
        ("models/user.py", "/app/models/user.py"),
        ("models/client.py", "/app/models/client.py"),
        ("models/device.py", "/app/models/device.py"),
        ("models/order.py", "/app/models/order.py"),
        ("models/part.py", "/app/models/part.py"),
        ("models/service.py", "/app/models/service.py"),
        ("models/service_item.py", "/app/models/service_item.py"),
        ("models/cash_register.py", "/app/models/cash_register.py"),
        
        # Routes
        ("routes/__init__.py", "/app/routes/__init__.py"),
        ("routes/auth.py", "/app/routes/auth.py"),
        ("routes/dashboard.py", "/app/routes/dashboard.py"),
        ("routes/clients.py", "/app/routes/clients.py"),
        ("routes/orders.py", "/app/routes/orders.py"),
        ("routes/parts.py", "/app/routes/parts.py"),
        ("routes/devices.py", "/app/routes/devices.py"),
        ("routes/archive.py", "/app/routes/archive.py"),
        ("routes/services.py", "/app/routes/services.py"),
        ("routes/devtools.py", "/app/routes/devtools.py"),
        
        # Templates
        ("templates/base.html", "/app/templates/base.html"),
        ("templates/dashboard.html", "/app/templates/dashboard.html"),
        ("templates/clients.html", "/app/templates/clients.html"),
        ("templates/orders.html", "/app/templates/orders.html"),
        ("templates/parts.html", "/app/templates/parts.html"),
        ("templates/devices.html", "/app/templates/devices.html"),
        ("templates/archive.html", "/app/templates/archive.html"),
        ("templates/services.html", "/app/templates/services.html"),
        ("templates/login.html", "/app/templates/login.html"),
        ("templates/welcome.html", "/app/templates/welcome.html"),
        ("templates/register_center.html", "/app/templates/register_center.html"),
        ("templates/register_service.html", "/app/templates/register_service.html"),
        ("templates/join_service.html", "/app/templates/join_service.html"),
        ("templates/users.html", "/app/templates/users.html"),
        ("templates/devtools.html", "/app/templates/devtools.html"),
        
        # Static CSS
        ("static/css/style.css", "/app/static/css/style.css"),
        ("static/css/modern.css", "/app/static/css/modern.css"),
        ("static/css/devtools.css", "/app/static/css/devtools.css"),
        
        # Static JS
        ("static/js/main.js", "/app/static/js/main.js"),
    ]
    
    success_count = 0
    total_count = len(files_to_sync)
    
    print(f"📁 Синхронизирую {total_count} файлов...")
    
    for local_path, server_path in files_to_sync:
        if os.path.exists(local_path):
            if upload_file(local_path, server_path):
                success_count += 1
        else:
            print(f"⚠️  Файл не найден: {local_path}")
    
    print(f"\n📊 Результат: {success_count}/{total_count} файлов синхронизировано")
    
    if success_count > 0:
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
                print("🎉 Полная синхронизация завершена! Сервер работает!")
                print("🌐 Проверьте https://miservis27.ru/dashboard")
            else:
                print("❌ Flask приложение не запустилось")
        else:
            print(f"❌ Ошибка запуска: {start_result.stderr}")
    else:
        print("❌ Ни один файл не был синхронизирован")

if __name__ == "__main__":
    full_sync()
