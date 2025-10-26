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

def check_app_structure():
    """Проверить структуру приложения"""
    print("🔍 Проверяю структуру приложения...")
    
    # Проверим app.py
    print("📋 Проверяю app.py...")
    app_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && cat app.py'")
    print(f"app.py:\n{app_content.stdout}")
    
    # Проверим routes/__init__.py
    print("📋 Проверяю routes/__init__.py...")
    routes_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && cat routes/__init__.py'")
    print(f"routes/__init__.py:\n{routes_content.stdout}")
    
    # Проверим маршруты
    print("🔍 Проверяю маршруты...")
    routes_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from app import app; print(\\\"Маршруты:\\\"); [print(rule) for rule in app.url_map.iter_rules()]\"'")
    print(f"Маршруты: {routes_check.stdout}")
    
    if routes_check.stderr:
        print(f"Ошибки маршрутов: {routes_check.stderr}")
    
    # Проверим доступность корневого маршрута
    print("🔍 Проверяю корневой маршрут...")
    root_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'curl -s http://localhost:8080/ || echo \"Корневой маршрут недоступен\"'")
    print(f"Корневой маршрут: {root_check.stdout}")

if __name__ == "__main__":
    check_app_structure()
