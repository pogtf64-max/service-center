#!/usr/bin/env python3
import subprocess
import os
import json

def run_ssh_command(command):
    """Выполнить SSH команду"""
    ssh_key = os.path.expanduser(r"~\.ssh\service_center")
    ssh_host = "root@77.110.127.57"
    
    cmd = ["ssh", "-i", ssh_key, ssh_host, command]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result

def professional_diagnosis():
    """Профессиональная диагностика проблемы 404"""
    print("🔍 ПРОФЕССИОНАЛЬНАЯ ДИАГНОСТИКА СЕРВЕРА")
    print("=" * 50)
    
    # 1. Проверяем статус всех сервисов
    print("\n1️⃣ ПРОВЕРКА СЕРВИСОВ:")
    services = run_ssh_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    print(services.stdout)
    
    # 2. Проверяем Nginx конфигурацию
    print("\n2️⃣ ПРОВЕРКА NGINX:")
    nginx_config = run_ssh_command("docker exec service-center-nginx-1 cat /etc/nginx/nginx.conf")
    print("Nginx конфигурация:")
    print(nginx_config.stdout)
    
    # 3. Проверяем доступность Flask напрямую
    print("\n3️⃣ ПРОВЕРКА FLASK (прямой доступ):")
    flask_direct = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/")
    print(f"Flask прямой доступ (порт 8080): {flask_direct.stdout}")
    
    # 4. Проверяем доступность через Nginx
    print("\n4️⃣ ПРОВЕРКА ЧЕРЕЗ NGINX:")
    nginx_access = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:80/")
    print(f"Nginx доступ (порт 80): {nginx_access.stdout}")
    
    # 5. Проверяем логи Nginx
    print("\n5️⃣ ЛОГИ NGINX:")
    nginx_logs = run_ssh_command("docker logs service-center-nginx-1 --tail 20")
    print(nginx_logs.stdout)
    
    # 6. Проверяем логи Flask
    print("\n6️⃣ ЛОГИ FLASK:")
    flask_logs = run_ssh_command("docker logs service-center-service-center-1 --tail 20")
    print(flask_logs.stdout)
    
    # 7. Проверяем сетевые подключения
    print("\n7️⃣ СЕТЕВЫЕ ПОДКЛЮЧЕНИЯ:")
    netstat = run_ssh_command("netstat -tlnp | grep -E ':(80|8080|9000)'")
    print(netstat.stdout)
    
    # 8. Проверяем маршруты Flask
    print("\n8️⃣ МАРШРУТЫ FLASK:")
    routes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from app import app; print(\\\"Маршруты:\\\"); [print(f\\\"{rule.rule} -> {rule.endpoint}\\\") for rule in app.url_map.iter_rules()]\"'")
    print(routes.stdout)
    
    # 9. Тестируем конкретные маршруты
    print("\n9️⃣ ТЕСТИРОВАНИЕ МАРШРУТОВ:")
    test_routes = [
        ("/", "Корневой маршрут"),
        ("/dashboard", "Dashboard"),
        ("/login", "Логин"),
        ("/dashboard/dashboard", "Dashboard blueprint")
    ]
    
    for route, description in test_routes:
        test_result = run_ssh_command(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8080{route}")
        print(f"{description} ({route}): {test_result.stdout}")
    
    # 10. Проверяем внешний доступ
    print("\n🔟 ВНЕШНИЙ ДОСТУП:")
    external_test = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' https://miservis27.ru/")
    print(f"Внешний доступ (https://miservis27.ru/): {external_test.stdout}")

if __name__ == "__main__":
    professional_diagnosis()
