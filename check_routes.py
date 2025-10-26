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

def check_routes():
    """Проверить маршруты Flask"""
    print("🔍 Проверяю маршруты Flask...")
    
    # Проверим статус контейнера
    status = run_ssh_command("docker ps | grep service-center-service-center-1")
    print(f"Статус: {status.stdout}")
    
    # Проверим логи
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 20")
    print(f"Логи:\n{logs.stdout}")
    
    # Проверим доступность Flask
    flask_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'curl -s http://localhost:8080/ || echo \"Flask недоступен\"'")
    print(f"Flask доступность: {flask_check.stdout}")
    
    # Проверим маршруты
    routes_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from app import app; print(\\\"Маршруты:\\\"); [print(rule) for rule in app.url_map.iter_rules()]\"'")
    print(f"Маршруты: {routes_check.stdout}")
    
    # Проверим app.py
    app_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"import app; print(\\\"app.py загружен\\\")\"'")
    print(f"app.py: {app_check.stdout}")

if __name__ == "__main__":
    check_routes()
