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

def diagnose_502():
    """Диагностировать ошибку 502"""
    print("🔍 Диагностирую ошибку 502...")
    
    # Проверим статус контейнеров
    print("📊 Статус контейнеров:")
    status = run_ssh_command("docker ps")
    print(status.stdout)
    
    # Проверим логи Flask приложения
    print("📋 Логи Flask приложения:")
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 30")
    print(logs.stdout)
    if logs.stderr:
        print(f"Ошибки: {logs.stderr}")
    
    # Проверим логи Nginx
    print("📋 Логи Nginx:")
    nginx_logs = run_ssh_command("docker logs service-center-nginx-1 --tail 20")
    print(nginx_logs.stdout)
    if nginx_logs.stderr:
        print(f"Ошибки Nginx: {nginx_logs.stderr}")
    
    # Проверим доступность Flask приложения
    print("🔗 Проверяю доступность Flask:")
    flask_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'curl -s http://localhost:8080 || echo \"Flask недоступен\"'")
    print(f"Flask ответ: {flask_check.stdout}")
    
    # Проверим процессы в контейнере
    print("⚙️ Процессы в контейнере:")
    processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux'")
    print(processes.stdout)

if __name__ == "__main__":
    diagnose_502()
