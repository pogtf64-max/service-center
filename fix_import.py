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

def fix_import():
    """Исправить импорт services"""
    print("🔧 Исправляю импорт services...")
    
    # Проверим содержимое routes/services.py
    services_content = run_ssh_command("docker exec -i service-center-service-center-1 bash -c 'cd /app && cat routes/services.py'")
    print(f"Содержимое routes/services.py:\n{services_content.stdout}")
    
    # Создадим правильный routes/services.py
    correct_services = '''from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.service_item import ServiceItem
from models.database import db
from flask_login import login_required, current_user

services = Blueprint('services', __name__)

@services.route('/')
@login_required
def index():
    services_list = ServiceItem.query.filter_by(service_id=current_user.service_id).all()
    return render_template('services.html', services=services_list)

@services.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        
        service_item = ServiceItem(
            name=name,
            description=description,
            price=price,
            service_id=current_user.service_id
        )
        
        db.session.add(service_item)
        db.session.commit()
        
        flash('Услуга успешно добавлена!', 'success')
        return redirect(url_for('services.index'))
    
    return render_template('add_service.html')

@services.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    service_item = ServiceItem.query.get_or_404(id)
    
    if request.method == 'POST':
        service_item.name = request.form.get('name')
        service_item.description = request.form.get('description')
        service_item.price = float(request.form.get('price', 0))
        
        db.session.commit()
        flash('Услуга успешно обновлена!', 'success')
        return redirect(url_for('services.index'))
    
    return render_template('edit_service.html', service=service_item)

@services.route('/delete/<int:id>')
@login_required
def delete(id):
    service_item = ServiceItem.query.get_or_404(id)
    db.session.delete(service_item)
    db.session.commit()
    
    flash('Услуга успешно удалена!', 'success')
    return redirect(url_for('services.index'))
'''
    
    # Остановим контейнер
    print("🛑 Останавливаю контейнер...")
    stop_result = run_ssh_command("docker stop service-center-service-center-1")
    
    # Создадим правильный файл
    print("📝 Создаю правильный routes/services.py...")
    create_cmd = f"cat > /tmp/services_correct.py << 'EOF'\n{correct_services}\nEOF"
    create_result = run_ssh_command(create_cmd)
    
    if create_result.returncode == 0:
        # Скопируем в контейнер
        print("📋 Копирую файл в контейнер...")
        copy_result = run_ssh_command("docker cp /tmp/services_correct.py service-center-service-center-1:/app/routes/services.py")
        
        if copy_result.returncode == 0:
            print("✅ Файл скопирован!")
            
            # Запустим контейнер
            print("🚀 Запускаю контейнер...")
            start_result = run_ssh_command("docker start service-center-service-center-1")
            
            if start_result.returncode == 0:
                print("✅ Контейнер запущен!")
                
                # Подождем
                import time
                time.sleep(5)
                
                # Проверим логи
                logs = run_ssh_command("docker logs service-center-service-center-1 --tail 10")
                print(f"Логи: {logs.stdout}")
                
                if "Running on" in logs.stdout:
                    print("🎉 Flask приложение запущено! Ошибка 502 исправлена!")
                else:
                    print("❌ Flask приложение все еще не запускается")
            else:
                print(f"❌ Ошибка запуска: {start_result.stderr}")
        else:
            print(f"❌ Ошибка копирования: {copy_result.stderr}")
    else:
        print(f"❌ Ошибка создания файла: {create_result.stderr}")

if __name__ == "__main__":
    fix_import()
