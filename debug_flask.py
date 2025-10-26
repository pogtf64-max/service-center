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

def debug_flask():
    """Отладить Flask приложение"""
    print("🔍 Отладка Flask приложения...")
    
    # Проверим процессы
    processes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ps aux | grep python'")
    print(f"Процессы Python: {processes.stdout}")
    
    # Проверим порты
    ports = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'netstat -tlnp | grep 8080'")
    print(f"Порты: {ports.stdout}")
    
    # Проверим логи подробно
    logs = run_ssh_command("docker logs service-center-service-center-1 --tail 50")
    print(f"Подробные логи:\n{logs.stdout}")
    
    if logs.stderr:
        print(f"Ошибки:\n{logs.stderr}")
    
    # Попробуем запустить Flask вручную
    print("🚀 Пробую запустить Flask вручную...")
    manual_start = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from app import app; app.run(host=\\\"0.0.0.0\\\", port=8080, debug=True)\"' &")
    print(f"Ручной запуск: {manual_start.stdout}")

if __name__ == "__main__":
    debug_flask()
