#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd):
    """Выполнить команду"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    return result

def sync_file(local_path, server_path):
    """Синхронизировать файл"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    # Копируем на сервер
    scp_cmd = f'scp -i "{ssh_key}" "{local_path}" {ssh_host}:/tmp/'
    scp_result = run_command(scp_cmd)
    
    if scp_result.returncode == 0:
        # Копируем в контейнер
        copy_cmd = f'ssh -i "{ssh_key}" {ssh_host} "docker cp /tmp/{os.path.basename(local_path)} service-center-service-center-1:{server_path}"'
        copy_result = run_command(copy_cmd)
        
        if copy_result.returncode == 0:
            print(f"✅ {local_path}")
            return True
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
            return False
    else:
        print(f"❌ Ошибка scp: {scp_result.stderr}")
        return False

def main():
    print("🚀 Синхронизирую файлы...")
    
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
            if sync_file(local, server):
                success += 1
        else:
            print(f"⚠️  Не найден: {local}")
    
    print(f"\n📊 Синхронизировано: {success}/{len(files)} файлов")
    
    if success > 0:
        print("🔄 Перезапускаю контейнер...")
        restart_cmd = f'ssh -i "{os.path.expanduser(r"~\.ssh\service_center")}" root@77.110.127.57 "docker restart service-center-service-center-1"'
        restart_result = run_command(restart_cmd)
        
        if restart_result.returncode == 0:
            print("✅ Контейнер перезапущен!")
            print("🎉 Синхронизация завершена!")
        else:
            print(f"❌ Ошибка перезапуска: {restart_result.stderr}")

if __name__ == "__main__":
    main()
