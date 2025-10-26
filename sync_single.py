#!/usr/bin/env python3
import subprocess
import os
import sys

def sync_single_file(local_path, server_path):
    """Синхронизировать один файл с сервера"""
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
    
    # Загружаем файл на сервер через echo
    cmd = [
        "ssh",
        "-i", ssh_key,
        ssh_host,
        f"echo '{content}' > {temp_file}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        # Копируем файл в контейнер
        copy_cmd = [
            "ssh",
            "-i", ssh_key,
            ssh_host,
            f"docker cp {temp_file} service-center-service-center-1:{server_path}"
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python sync_single.py <local_path> <server_path>")
        sys.exit(1)
    
    local_path = sys.argv[1]
    server_path = sys.argv[2]
    
    if sync_single_file(local_path, server_path):
        print("✅ Файл синхронизирован успешно!")
    else:
        print("❌ Ошибка синхронизации файла!")
        sys.exit(1)
