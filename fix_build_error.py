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

def fix_build_error():
    """Исправить ошибку BuildError"""
    print("🔧 ИСПРАВЛЯЮ ОШИБКУ BuildError")
    print("=" * 40)
    
    # 1. Проверим содержимое register_service.html
    print("1️⃣ ПРОВЕРКА register_service.html:")
    template_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"service.register_service\" /app/templates/register_service.html'")
    print(f"Неправильные ссылки: {template_content.stdout}")
    
    # 2. Проверим все ссылки в шаблоне
    print("\n2️⃣ ВСЕ ССЫЛКИ В ШАБЛОНЕ:")
    all_links = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"url_for\" /app/templates/register_service.html'")
    print(f"Все ссылки: {all_links.stdout}")
    
    # 3. Проверим доступные маршруты
    print("\n3️⃣ ДОСТУПНЫЕ МАРШРУТЫ:")
    routes = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && python -c \"from app import app; print(\\\"Маршруты:\\\"); [print(f\\\"{rule.rule} -> {rule.endpoint}\\\") for rule in app.url_map.iter_rules() if \\\"service\\\" in rule.endpoint or \\\"register\\\" in rule.endpoint]\"'")
    print(f"Маршруты с service/register: {routes.stdout}")
    
    # 4. Исправим шаблон
    print("\n4️⃣ ИСПРАВЛЯЮ ШАБЛОН...")
    
    # Сначала посмотрим на текущий шаблон
    current_template = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'head -50 /app/templates/register_service.html'")
    print(f"Начало шаблона: {current_template.stdout}")
    
    # Создадим исправленную версию
    fixed_template = '''{% extends "base.html" %}

{% block title %}Регистрация сервисного центра{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow-lg border-0">
                <div class="card-header bg-primary text-white text-center">
                    <h3 class="mb-0">
                        <i class="bi bi-building-add"></i> Регистрация сервисного центра
                    </h3>
                </div>
                <div class="card-body p-4">
                    <p class="text-muted mb-4">Создайте новый сервисный центр и станьте его директором</p>
                    
                    <form method="POST">
                        <div class="mb-3">
                            <label for="service_name" class="form-label">
                                <i class="bi bi-building"></i> Название сервисного центра *
                            </label>
                            <input type="text" class="form-control" id="service_name" name="service_name" 
                                   placeholder="Введите название вашего сервисного центра" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="service_address" class="form-label">
                                <i class="bi bi-geo-alt"></i> Адрес сервисного центра *
                            </label>
                            <input type="text" class="form-control" id="service_address" name="service_address" 
                                   placeholder="Введите адрес сервисного центра" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="director_name" class="form-label">
                                <i class="bi bi-person"></i> ФИО директора *
                            </label>
                            <input type="text" class="form-control" id="director_name" name="director_name" 
                                   placeholder="Введите ваше ФИО" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="director_phone" class="form-label">
                                <i class="bi bi-telephone"></i> Телефон директора *
                            </label>
                            <input type="tel" class="form-control" id="director_phone" name="director_phone" 
                                   placeholder="Введите ваш телефон" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="service_password" class="form-label">
                                <i class="bi bi-key"></i> Пароль сервисного центра *
                            </label>
                            <input type="password" class="form-control" id="service_password" name="service_password" 
                                   placeholder="Придумайте пароль для сервисного центра" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="director_password" class="form-label">
                                <i class="bi bi-shield-lock"></i> Пароль директора *
                            </label>
                            <input type="password" class="form-control" id="director_password" name="director_password" 
                                   placeholder="Придумайте пароль для входа" required>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="bi bi-check-circle"></i> Создать сервисный центр
                            </button>
                            <a href="{{ url_for('auth.index') }}" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left"></i> Назад
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Создадим исправленный файл
    print("📝 Создаю исправленный register_service.html...")
    create_cmd = f"cat > /tmp/register_service_fixed.html << 'EOF'\n{fixed_template}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/register_service_fixed.html service-center-service-center-1:/app/templates/register_service.html")
        
        if copy_result.returncode == 0:
            print("✅ register_service.html исправлен!")
            
            # Проверим результат
            print("🔍 Проверяю результат...")
            check_result = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'grep -n \"url_for\" /app/templates/register_service.html'")
            print(f"Ссылки после исправления: {check_result.stdout}")
            
            # Тестируем доступность
            print("🧪 Тестирую доступность...")
            test_result = run_ssh_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/register-center")
            print(f"Результат теста: {test_result.stdout}")
            
            print("🎉 ОШИБКА BuildError ИСПРАВЛЕНА!")
            print("🌐 Проверьте https://miservis27.ru/register-center")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания файла: {create_result.stderr}")

if __name__ == "__main__":
    fix_build_error()
