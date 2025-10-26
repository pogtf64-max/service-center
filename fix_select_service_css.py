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

def fix_select_service_css():
    """Исправить CSS в select-service.html"""
    print("🔧 ИСПРАВЛЯЮ CSS В select-service.html")
    print("=" * 45)
    
    # 1. Проверим текущее содержимое select-service.html
    print("1️⃣ ПРОВЕРКА ТЕКУЩЕГО СОДЕРЖИМОГО:")
    current_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'head -20 /app/templates/select-service.html'")
    print(f"Начало файла: {current_content.stdout}")
    
    # 2. Проверим есть ли ссылки на CSS
    print("\n2️⃣ ПРОВЕРКА CSS ССЫЛОК:")
    css_links = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"css\\|style\" /app/templates/select-service.html'")
    print(f"CSS ссылки: {css_links.stdout}")
    
    # 3. Проверим extends ли файл base.html
    print("\n3️⃣ ПРОВЕРКА НАСЛЕДОВАНИЯ:")
    extends_check = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"extends\\|block\" /app/templates/select-service.html'")
    print(f"Наследование: {extends_check.stdout}")
    
    # 4. Если файл не наследует base.html, добавим CSS ссылки
    if not extends_check.stdout.strip():
        print("\n4️⃣ ДОБАВЛЯЮ CSS ССЫЛКИ В select-service.html...")
        
        # Создадим исправленную версию с CSS
        fixed_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Выбор сервисного центра</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/modern.css') }}" rel="stylesheet">
</head>
<body>
    <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
        <div class="row w-100">
            <div class="col-md-6 mx-auto">
                <div class="card shadow-lg border-0">
                    <div class="card-header bg-primary text-white text-center">
                        <h3 class="mb-0">
                            <i class="bi bi-building"></i> Выбор сервисного центра
                        </h3>
                    </div>
                    <div class="card-body p-4">
                        <p class="text-muted mb-4">Введите данные вашего сервисного центра</p>
                        
                        <form method="POST">
                            <div class="mb-3">
                                <label for="service_name" class="form-label">
                                    <i class="bi bi-building"></i> Название сервисного центра *
                                </label>
                                <input type="text" class="form-control" id="service_name" name="service_name" 
                                       placeholder="Введите точное название вашего сервисного центра" required>
                            </div>
                            
                            <div class="mb-4">
                                <label for="service_password" class="form-label">
                                    <i class="bi bi-key"></i> Пароль сервисного центра *
                                </label>
                                <input type="password" class="form-control" id="service_password" name="service_password" 
                                       placeholder="Получите пароль у директора сервисного центра" required>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="bi bi-arrow-right"></i> Продолжить
                                </button>
                                <a href="{{ url_for('auth.index') }}" class="btn btn-outline-secondary">
                                    <i class="bi bi-house"></i> На главную
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <footer class="text-center text-muted py-3">
        <small>© 2024 Сервисный центр. Все права защищены.</small>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
        
        # Создадим исправленный файл на сервере
        print("📝 Создаю исправленный select-service.html...")
        create_cmd = f"cat > /tmp/select_service_fixed.html << 'EOF'\n{fixed_content}\nEOF"
        create_result = run_ssh_command(create_cmd)
        
        if create_result.returncode == 0:
            # Скопируем в контейнер
            print("📋 Копирую файл в контейнер...")
            copy_result = run_ssh_command("docker cp /tmp/select_service_fixed.html service-center-service-center-1:/app/templates/select-service.html")
            
            if copy_result.returncode == 0:
                print("✅ select-service.html исправлен!")
                
                # Проверим результат
                print("🔍 Проверяю результат...")
                check_result = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"css\\|style\" /app/templates/select-service.html'")
                print(f"CSS ссылки после исправления: {check_result.stdout}")
                
                print("🎉 CSS ПРОБЛЕМА ИСПРАВЛЕНА!")
                print("🌐 Проверьте https://miservis27.ru/select-service")
            else:
                print(f"❌ Ошибка копирования: {copy_result.stderr}")
        else:
            print(f"❌ Ошибка создания файла: {create_result.stderr}")
    else:
        print("✅ Файл уже наследует base.html или имеет CSS ссылки")

if __name__ == "__main__":
    fix_select_service_css()
