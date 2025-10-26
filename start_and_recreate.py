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

def start_and_recreate():
    """Запустить контейнер и пересоздать БД"""
    print("🚀 Запускаю контейнер и пересоздаю БД...")
    
    # Запустим контейнер
    print("🚀 Запускаю контейнер...")
    start_result = run_ssh_command("docker start service-center-service-center-1")
    
    if start_result.returncode == 0:
        print("✅ Контейнер запущен!")
        
        # Подождем
        time.sleep(3)
        
        # Запустим скрипт пересоздания БД
        print("🔧 Запускаю скрипт пересоздания БД...")
        run_script = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python recreate_db.py'")
        print(f"Результат: {run_script.stdout}")
        
        if run_script.stderr:
            print(f"Ошибки: {run_script.stderr}")
        
        if run_script.returncode == 0:
            print("✅ База данных пересоздана!")
            
            # Перезапустим контейнер
            print("🔄 Перезапускаю контейнер...")
            restart_result = run_ssh_command("docker restart service-center-service-center-1")
            
            if restart_result.returncode == 0:
                print("✅ Контейнер перезапущен!")
                
                # Подождем
                time.sleep(5)
                
                # Проверим логи
                logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
                print(f"Логи: {logs.stdout}")
                
                if "Running on" in logs.stdout:
                    print("🎉 Flask приложение запущено! База данных исправлена!")
                    print("🌐 Проверьте https://miservis27.ru/dashboard")
                else:
                    print("❌ Flask приложение все еще не запускается")
            else:
                print(f"❌ Ошибка перезапуска: {restart_result.stderr}")
        else:
            print(f"❌ Ошибка выполнения скрипта: {run_script.stderr}")
    else:
        print(f"❌ Ошибка запуска: {start_result.stderr}")

if __name__ == "__main__":
    start_and_recreate()
