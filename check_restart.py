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

def check_restart():
    """Проверить почему контейнер перезапускается"""
    print("🔍 Проверяю почему контейнер перезапускается...")
    
    # Проверим статус
    status = run_ssh_command("docker ps | grep service-center-service-center-1")
    print(f"Статус: {status.stdout}")
    
    # Проверим логи
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 30")
    print(f"Логи:\n{logs.stdout}")
    
    if logs.stderr:
        print(f"Ошибки:\n{logs.stderr}")
    
    # Проверим app.py
    app_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"import app; print(\\\"app.py загружен\\\")\"' 2>&1")
    print(f"Проверка app.py: {app_check.stdout}")
    
    # Проверим синтаксис
    syntax_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -m py_compile app.py 2>&1'")
    print(f"Синтаксис app.py: {syntax_check.stdout}")

if __name__ == "__main__":
    check_restart()
