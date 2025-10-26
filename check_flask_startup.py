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

def check_flask_startup():
    """Проверить запуск Flask"""
    print("🔍 ПРОВЕРКА ЗАПУСКА FLASK")
    print("=" * 40)
    
    # 1. Проверим процессы внутри контейнера
    print("\n1️⃣ ПРОЦЕССЫ В КОНТЕЙНЕРЕ:")
    processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux'")
    print(f"Процессы: {processes.stdout}")
    
    # 2. Проверим запущен ли Flask
    print("\n2️⃣ ПРОВЕРКА FLASK:")
    flask_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'pgrep -f python'")
    print(f"Python процессы: {flask_check.stdout}")
    
    # 3. Проверим порт 8080
    print("\n3️⃣ ПРОВЕРКА ПОРТА 8080:")
    port_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'netstat -tlnp | grep 8080'")
    print(f"Порт 8080: {port_check.stdout}")
    
    # 4. Попробуем запустить Flask вручную
    print("\n4️⃣ РУЧНОЙ ЗАПУСК FLASK:")
    manual_start = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python app.py &'")
    print(f"Ручной запуск: {manual_start.stdout}")
    
    # Подождем немного
    import time
    time.sleep(3)
    
    # 5. Проверим снова процессы
    print("\n5️⃣ ПРОВЕРКА ПОСЛЕ РУЧНОГО ЗАПУСКА:")
    processes_after = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux | grep python'")
    print(f"Процессы после запуска: {processes_after.stdout}")
    
    # 6. Проверим логи после запуска
    print("\n6️⃣ ЛОГИ ПОСЛЕ ЗАПУСКА:")
    logs_after = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
    print(f"Логи: {logs_after.stdout}")
    
    # 7. Проверим доступность
    print("\n7️⃣ ПРОВЕРКА ДОСТУПНОСТИ:")
    access_test = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/")
    print(f"Доступность: {access_test.stdout}")
    
    # 8. Проверим есть ли ошибки в app.py
    print("\n8️⃣ ПРОВЕРКА СИНТАКСИСА app.py:")
    syntax_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -m py_compile app.py'")
    print(f"Синтаксис: {syntax_check.stdout}")
    if syntax_check.stderr:
        print(f"Ошибки синтаксиса: {syntax_check.stderr}")

if __name__ == "__main__":
    check_flask_startup()
