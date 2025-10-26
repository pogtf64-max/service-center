#!/usr/bin/env python3
import subprocess
import os
import time

def run_ssh_command(command):
    """Выполнить SSH команду"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    cmd = ["ssh", "-i", ssh_key, ssh_host, command]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result

def check_status():
    """Проверить статус сервера"""
    print("🔍 Проверяю статус сервера...")
    
    # Проверим статус контейнера
    status = run_ssh_command("docker ps | grep service-center-service-center-1")
    print(f"Статус контейнера: {status.stdout}")
    
    # Подождем немного
    time.sleep(3)
    
    # Проверим логи
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 20")
    print(f"Логи: {logs.stdout}")
    
    if logs.stderr:
        print(f"Ошибки: {logs.stderr}")
    
    # Проверим доступность Flask
    flask_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'curl -s http://localhost:8080 || echo \"Flask недоступен\"'")
    print(f"Flask доступность: {flask_check.stdout}")
    
    # Проверим процессы
    processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux | grep python'")
    print(f"Процессы Python: {processes.stdout}")

if __name__ == "__main__":
    check_status()
