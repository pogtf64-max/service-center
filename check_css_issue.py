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

def check_css_issue():
    """Проверить проблему с CSS"""
    print("🔍 ПРОВЕРКА ПРОБЛЕМЫ С CSS")
    print("=" * 40)
    
    # 1. Проверим структуру статических файлов
    print("\n1️⃣ СТРУКТУРА СТАТИЧЕСКИХ ФАЙЛОВ:")
    static_structure = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'find /app/static -type f -name \"*.css\" | head -10'")
    print(f"CSS файлы: {static_structure.stdout}")
    
    # 2. Проверим доступность CSS через Flask
    print("\n2️⃣ ДОСТУПНОСТЬ CSS ЧЕРЕЗ FLASK:")
    css_test = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/static/css/style.css")
    print(f"style.css через Flask: {css_test.stdout}")
    
    # 3. Проверим доступность CSS через Nginx
    print("\n3️⃣ ДОСТУПНОСТЬ CSS ЧЕРЕЗ NGINX:")
    nginx_css_test = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:9000/static/css/style.css")
    print(f"style.css через Nginx: {nginx_css_test.stdout}")
    
    # 4. Проверим содержимое select-service.html
    print("\n4️⃣ ПРОВЕРКА select-service.html:")
    select_service = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"style.css\" /app/templates/select-service.html'")
    print(f"Ссылки на CSS в select-service.html: {select_service.stdout}")
    
    # 5. Проверим base.html
    print("\n5️⃣ ПРОВЕРКА base.html:")
    base_css = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"style.css\" /app/templates/base.html'")
    print(f"Ссылки на CSS в base.html: {base_css.stdout}")
    
    # 6. Проверим логи Nginx для статических файлов
    print("\n6️⃣ ЛОГИ NGINX ДЛЯ СТАТИЧЕСКИХ ФАЙЛОВ:")
    nginx_logs = run_ssh_command("docker logs service-center-nginx-1 --tail 20 | grep -E '(static|css|style)'")
    print(f"Логи статических файлов: {nginx_logs.stdout}")
    
    # 7. Проверим права доступа к файлам
    print("\n7️⃣ ПРАВА ДОСТУПА К CSS ФАЙЛАМ:")
    permissions = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'ls -la /app/static/css/'")
    print(f"Права доступа: {permissions.stdout}")
    
    # 8. Тестируем прямой доступ к CSS
    print("\n8️⃣ ТЕСТИРОВАНИЕ ПРЯМОГО ДОСТУПА:")
    direct_css = run_ssh_command("curl -s -I http://localhost:8080/static/css/style.css")
    print(f"Заголовки CSS: {direct_css.stdout}")

if __name__ == "__main__":
    check_css_issue()
