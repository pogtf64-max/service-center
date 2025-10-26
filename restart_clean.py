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

def restart_clean():
    """Чистый перезапуск контейнера"""
    print("🔄 Чистый перезапуск контейнера...")
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    
    # Удалим кэш Python
    print("🗑️ Удаляю кэш Python...")
    rm_cache = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'rm -rf /app/__pycache__ /app/models/__pycache__ /app/routes/__pycache__'")
    
    # Запустим контейнер
    print("🚀 Запускаю контейнер...")
    start_result = run_ssh_command("docker start service-center-service-center-1")
    
    if start_result.returncode == 0:
        print("✅ Контейнер запущен!")
        
        # Подождем
        time.sleep(5)
        
        # Проверим статус
        status = run_ssh_command("docker ps | grep service-center-service-center-1")
        print(f"Статус: {status.stdout}")
        
        # Проверим логи
        logs = run_ssh_command("docker logs service-center-service-center-1 --tail 15")
        print(f"Логи: {logs.stdout}")
        
        if "Running on" in logs.stdout:
            print("🎉 Flask приложение запущено!")
            
            # Проверим доступность
            flask_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'curl -s http://localhost:8080/ || echo \"Flask недоступен\"'")
            print(f"Flask доступность: {flask_check.stdout}")
            
            if "Flask недоступен" not in flask_check.stdout:
                print("✅ Flask приложение доступно!")
                print("🌐 Проверьте https://miservis27.ru/dashboard")
            else:
                print("❌ Flask приложение все еще недоступно")
        else:
            print("❌ Flask приложение не запустилось")
    else:
        print(f"❌ Ошибка запуска: {start_result.stderr}")

if __name__ == "__main__":
    restart_clean()
