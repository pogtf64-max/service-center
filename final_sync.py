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
    
    # Читаем файл
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Экранируем кавычки
    content = content.replace("'", "'\"'\"'")
    
    # Загружаем через echo
    cmd = f"echo '{content}' > /tmp/{os.path.basename(local_path)}"
    result = run_ssh_command(cmd)
    
    if result.returncode == 0:
        # Копируем в контейнер
        copy_cmd = f"docker cp /tmp/{os.path.basename(local_path)} service-center-service-center-1:{server_path}"
        copy_result = run_ssh_command(copy_cmd)
        
        if copy_result.returncode == 0:
            print(f"✅ {local_path}")
            return True
        else:
            print(f"❌ Ошибка копирования {local_path}: {copy_result.stderr}")
            return False
    else:
        print(f"❌ Ошибка загрузки {local_path}: {result.stderr}")
        return False

def main():
    print("🚀 Синхронизирую файлы с сервера...")
    
    files = [
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
    
    success = 0
    for local, server in files:
        if os.path.exists(local):
            if upload_file(local, server):
                success += 1
        else:
            print(f"⚠️  Не найден: {local}")
    
    print(f"\n📊 Синхронизировано: {success}/{len(files)} файлов")
    
    if success > 0:
        print("🔄 Перезапускаю контейнер...")
        restart = run_ssh_command("docker restart service-center-service-center-1")
        if restart.returncode == 0:
            print("✅ Контейнер перезапущен!")
            print("🎉 Синхронизация завершена!")
        else:
            print(f"❌ Ошибка перезапуска: {restart.stderr}")

if __name__ == "__main__":
    main()
