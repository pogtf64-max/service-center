#!/usr/bin/env python3
import subprocess
import os

def copy_file_to_server(local_path, server_path):
    """Копировать файл на сервер через scp"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    # Копируем файл на сервер
    scp_cmd = [
        "scp",
        "-i", ssh_key,
        local_path,
        f"{ssh_host}:/tmp/{os.path.basename(local_path)}"
    ]
    
    print(f"📤 Копирую {local_path} на сервер...")
    result = subprocess.run(scp_cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        # Копируем файл в контейнер
        copy_cmd = [
            "ssh",
            "-i", ssh_key,
            ssh_host,
            f"docker cp /tmp/{os.path.basename(local_path)} service-center-service-center-1:{server_path}"
        ]
        
        print(f"📦 Копирую в контейнер: {server_path}")
        copy_result = subprocess.run(copy_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if copy_result.returncode == 0:
            print(f"✅ {local_path} → {server_path}")
            return True
        else:
            print(f"❌ Ошибка копирования в контейнер: {copy_result.stderr}")
            return False
    else:
        print(f"❌ Ошибка копирования на сервер: {result.stderr}")
        return False

def main():
    # Список файлов для синхронизации
    files_to_sync = [
        ("templates/orders.html", "/app/templates/orders.html"),
        ("templates/parts.html", "/app/templates/parts.html"),
        ("templates/services.html", "/app/templates/services.html"),
        ("templates/devices.html", "/app/templates/devices.html"),
        ("templates/archive.html", "/app/templates/archive.html"),
        ("routes/orders.py", "/app/routes/orders.py"),
        ("routes/parts.py", "/app/routes/parts.py"),
        ("routes/services.py", "/app/routes/services.py"),
        ("routes/devices.py", "/app/routes/devices.py"),
        ("routes/archive.py", "/app/routes/archive.py"),
        ("models/service_item.py", "/app/models/service_item.py"),
        ("static/css/modern.css", "/app/static/css/modern.css"),
        ("app.py", "/app/app.py"),
    ]
    
    print("🚀 Начинаю синхронизацию файлов...")
    
    success_count = 0
    for local_path, server_path in files_to_sync:
        if os.path.exists(local_path):
            if copy_file_to_server(local_path, server_path):
                success_count += 1
        else:
            print(f"⚠️  Файл не найден: {local_path}")
    
    print(f"\n📊 Результат: {success_count} файлов синхронизировано")
    
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
            print("🎉 Синхронизация завершена!")
        else:
            print(f"❌ Ошибка перезапуска: {restart_result.stderr}")

if __name__ == "__main__":
    main()
