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

def check_loading_issue():
    """Проверить проблему с загрузкой сайта"""
    print("🔍 ДИАГНОСТИКА ПРОБЛЕМЫ ЗАГРУЗКИ")
    print("=" * 50)
    
    # 1. Проверим статус контейнеров
    print("\n1️⃣ СТАТУС КОНТЕЙНЕРОВ:")
    containers = run_ssh_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    print(containers.stdout)
    
    # 2. Проверим логи Flask (последние 30 строк)
    print("\n2️⃣ ЛОГИ FLASK (последние 30 строк):")
    flask_logs = run_ssh_command("docker logs service-center-service-center-1 --tail 30")
    print(flask_logs.stdout)
    
    # 3. Проверим логи Nginx (последние 20 строк)
    print("\n3️⃣ ЛОГИ NGINX (последние 20 строк):")
    nginx_logs = run_ssh_command("docker logs service-center-nginx-1 --tail 20")
    print(nginx_logs.stdout)
    
    # 4. Проверим ошибки в логах
    print("\n4️⃣ ПОИСК ОШИБОК В ЛОГАХ:")
    error_logs = run_ssh_command("docker logs service-center-service-center-1 --tail 100 | grep -i 'error\\|exception\\|traceback\\|failed'")
    print(f"Ошибки Flask: {error_logs.stdout}")
    
    nginx_errors = run_ssh_command("docker logs service-center-nginx-1 --tail 50 | grep -i 'error\\|failed\\|timeout'")
    print(f"Ошибки Nginx: {nginx_errors.stdout}")
    
    # 5. Проверим доступность Flask
    print("\n5️⃣ ТЕСТИРОВАНИЕ ДОСТУПНОСТИ:")
    flask_test = run_ssh_command("curl -s -w 'HTTP: %{http_code}, Time: %{time_total}s' http://localhost:8080/")
    print(f"Flask прямой доступ: {flask_test.stdout}")
    
    # 6. Проверим доступность через Nginx
    nginx_test = run_ssh_command("curl -s -w 'HTTP: %{http_code}, Time: %{time_total}s' http://localhost:9000/")
    print(f"Nginx доступ: {nginx_test.stdout}")
    
    # 7. Проверим внешний доступ
    external_test = run_ssh_command("curl -s -w 'HTTP: %{http_code}, Time: %{time_total}s' https://miservis27.ru/")
    print(f"Внешний доступ: {external_test.stdout}")
    
    # 8. Проверим процессы Python
    print("\n6️⃣ ПРОЦЕССЫ PYTHON:")
    python_processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux | grep python'")
    print(f"Python процессы: {python_processes.stdout}")
    
    # 9. Проверим использование памяти
    print("\n7️⃣ ИСПОЛЬЗОВАНИЕ РЕСУРСОВ:")
    memory_usage = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'free -h'")
    print(f"Память: {memory_usage.stdout}")
    
    # 10. Проверим сетевые подключения
    print("\n8️⃣ СЕТЕВЫЕ ПОДКЛЮЧЕНИЯ:")
    network_connections = run_ssh_command("netstat -tlnp | grep -E ':(80|8080|9000)'")
    print(f"Сетевые подключения: {network_connections.stdout}")
    
    # 11. Проверим время ответа Flask
    print("\n9️⃣ ТЕСТИРОВАНИЕ ВРЕМЕНИ ОТВЕТА:")
    response_time = run_ssh_command("time curl -s http://localhost:8080/ > /dev/null")
    print(f"Время ответа Flask: {response_time.stdout}")
    
    # 12. Проверим есть ли зависшие запросы
    print("\n🔟 ПРОВЕРКА ЗАВИСШИХ ЗАПРОСОВ:")
    hanging_requests = run_ssh_command("docker logs service-center-service-center-1 --tail 50 | grep -E 'GET|POST' | tail -10")
    print(f"Последние запросы: {hanging_requests.stdout}")

if __name__ == "__main__":
    check_loading_issue()
