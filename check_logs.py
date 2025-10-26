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

def check_server_logs():
    """Проверить логи сервера"""
    print("🔍 Проверяю логи сервера...")
    
    # Проверим статус контейнера
    status = run_ssh_command("docker ps | grep service-center")
    print(f"Статус контейнера: {status.stdout}")
    
    # Проверим последние логи
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 50")
    print(f"Последние логи:\n{logs.stdout}")
    
    if logs.stderr:
        print(f"Ошибки:\n{logs.stderr}")
    
    # Проверим app.py
    app_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"import app; print(\\\"app.py загружен\\\")\"'")
    print(f"Проверка app.py: {app_check.stdout}")
    if app_check.stderr:
        print(f"Ошибка app.py: {app_check.stderr}")
    
    # Проверим routes
    routes_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from routes.dashboard import dashboard_bp; print(\\\"dashboard загружен\\\")\"'")
    print(f"Проверка dashboard: {routes_check.stdout}")
    if routes_check.stderr:
        print(f"Ошибка dashboard: {routes_check.stderr}")

if __name__ == "__main__":
    check_server_logs()
