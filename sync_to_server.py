#!/usr/bin/env python3
import subprocess
import os
import glob

def sync_file_to_server(local_path, server_path):
    """Синхронизировать файл с сервера"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    # Читаем локальный файл
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения {local_path}: {e}")
        return False
    
    # Загружаем файл на сервер
    cmd = [
        "ssh",
        "-i", ssh_key,
        ssh_host,
        f"cat > /tmp/{os.path.basename(local_path)} << 'EOF'\n{content}\nEOF"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        # Копируем файл в контейнер
        copy_cmd = [
            "ssh",
            "-i", ssh_key,
            ssh_host,
            f"docker cp /tmp/{os.path.basename(local_path)} service-center-service-center-1:{server_path}"
        ]
        
        copy_result = subprocess.run(copy_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if copy_result.returncode == 0:
            print(f"✅ {local_path} → {server_path}")
            return True
        else:
            print(f"❌ Ошибка копирования {local_path}: {copy_result.stderr}")
            return False
    else:
        print(f"❌ Ошибка загрузки {local_path}: {result.stderr}")
        return False

def sync_all_files():
    """Синхронизировать все файлы с сервера"""
    
    # Список файлов для синхронизации
    files_to_sync = [
        # Templates
        ("templates/dashboard.html", "/app/templates/dashboard.html"),
        ("templates/base.html", "/app/templates/base.html"),
        ("templates/clients.html", "/app/templates/clients.html"),
        ("templates/orders.html", "/app/templates/orders.html"),
        ("templates/parts.html", "/app/templates/parts.html"),
        ("templates/services.html", "/app/templates/services.html"),
        ("templates/devices.html", "/app/templates/devices.html"),
        ("templates/archive.html", "/app/templates/archive.html"),
        
        # Routes
        ("routes/dashboard.py", "/app/routes/dashboard.py"),
        ("routes/clients.py", "/app/routes/clients.py"),
        ("routes/orders.py", "/app/routes/orders.py"),
        ("routes/parts.py", "/app/routes/parts.py"),
        ("routes/services.py", "/app/routes/services.py"),
        ("routes/devices.py", "/app/routes/devices.py"),
        ("routes/archive.py", "/app/routes/archive.py"),
        
        # Models
        ("models/service_item.py", "/app/models/service_item.py"),
        
        # Static CSS
        ("static/css/modern.css", "/app/static/css/modern.css"),
        ("static/css/style.css", "/app/static/css/style.css"),
        
        # Main app
        ("app.py", "/app/app.py"),
    ]
    
    print("🚀 Начинаю синхронизацию файлов с сервера...")
    
    success_count = 0
    total_count = len(files_to_sync)
    
    for local_path, server_path in files_to_sync:
        if os.path.exists(local_path):
            if sync_file_to_server(local_path, server_path):
                success_count += 1
        else:
            print(f"⚠️  Файл не найден: {local_path}")
    
    print(f"\n📊 Результат: {success_count}/{total_count} файлов синхронизировано")
    
    if success_count > 0:
        print("🔄 Перезапускаю контейнер...")
        ssh_key = os.path.expanduser(r"~\.ssh\service_center")
        ssh_host = "root@77.110.127.57"
        
        restart_cmd = [
            "ssh",
            "-i", ssh_key,
            ssh_host,
            "docker restart service-center-service-center-1"
        ]
        
        restart_result = subprocess.run(restart_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if restart_result.returncode == 0:
            print("✅ Контейнер перезапущен!")
            print("🎉 Синхронизация завершена! Все изменения применены на сервере!")
        else:
            print(f"❌ Ошибка перезапуска: {restart_result.stderr}")
    else:
        print("❌ Ни один файл не был синхронизирован")

if __name__ == "__main__":
    sync_all_files()
