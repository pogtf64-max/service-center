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

def find_can_manage():
    """Найти все места где используется can_manage_settings"""
    print("🔍 Ищу все места где используется can_manage_settings...")
    
    # Поищем в коде
    search_result = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && grep -r \"can_manage_settings\" .'")
    print(f"Найденные места:\n{search_result.stdout}")
    
    if search_result.stderr:
        print(f"Ошибки поиска: {search_result.stderr}")
    
    # Проверим конкретные файлы
    files_to_check = [
        "models/user.py",
        "routes/auth.py", 
        "routes/dashboard.py",
        "routes/clients.py",
        "routes/orders.py",
        "routes/parts.py",
        "routes/devices.py",
        "routes/archive.py",
        "routes/services.py",
        "routes/devtools.py"
    ]
    
    for file_path in files_to_check:
        print(f"🔍 Проверяю {file_path}...")
        check_result = run_ssh_command(f"docker exec -i service-center-service-center-1 bash -c 'cd /app && grep -n \"can_manage_settings\" {file_path}'")
        if check_result.stdout:
            print(f"Найдено в {file_path}:\n{check_result.stdout}")

if __name__ == "__main__":
    find_can_manage()
