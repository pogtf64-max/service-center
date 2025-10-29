"""
Маршруты управления сервисом
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models.service import Service
from models.user import User
from models.database import db
from datetime import datetime

service_bp = Blueprint('service', __name__)

@service_bp.route('/register-service', methods=['GET', 'POST'])
def register_service():
    """Регистрация нового сервисного центра"""
    if request.method == 'POST':
        # Данные сервиса
        service_name = request.form['service_name']
        service_address = request.form.get('service_address', '')
        service_phone = request.form.get('service_phone', '')
        service_email = request.form.get('service_email', '')
        service_password = request.form['service_password']
        
        # Данные директора
        director_name = request.form['director_name']
        director_username = request.form['director_username']
        director_password = request.form['director_password']
        director_email = request.form.get('director_email', '')
        director_phone = request.form.get('director_phone', '')
        
        # Проверка уникальности имени пользователя
        if User.query.filter_by(username=director_username).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register_service.html')
        
        if Service.query.filter_by(name=service_name).first():
            flash('Сервис с таким названием уже существует', 'error')
            return render_template('register_service.html')
        
        # Создание директора сначала
        director = User(
            username=director_username,
            password_hash=generate_password_hash(director_password),
            role='director',
            full_name=director_name,
            email=director_email,
            phone=director_phone,
            is_active=True,
            is_approved=True  # Директор автоматически подтвержден
        )
        db.session.add(director)
        db.session.flush()  # Получаем ID директора
        
        # Создание сервиса с director_id
        service = Service(
            name=service_name,
            address=service_address,
            phone=service_phone,
            email=service_email,
            service_password=generate_password_hash(service_password),
            director_id=director.id
        )
        db.session.add(service)
        db.session.flush()  # Получаем ID сервиса
        
        # Обновляем service_id у директора
        director.service_id = service.id
        
        db.session.commit()
        
        # Автоматический вход директора в систему
        from flask_login import login_user
        login_user(director)
        
        flash(f'Сервис и директор успешно созданы! Добро пожаловать, {director_name}!', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('register_service.html')

@service_bp.route('/join-service', methods=['GET', 'POST'])
def join_service():
    """Присоединение к существующему сервису"""
    if request.method == 'POST':
        service_name = request.form['service_name']
        service_password = request.form['service_password']
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        role = request.form['role']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        
        # Поиск сервиса
        service = Service.query.filter_by(name=service_name).first()
        if not service:
            flash('Сервис не найден', 'error')
            return render_template('join_service.html')
        
        # Проверка пароля сервиса
        from werkzeug.security import check_password_hash
        if not check_password_hash(service.service_password, service_password):
            flash('Неверный пароль сервиса', 'error')
            return render_template('join_service.html')
        
        # Проверка уникальности пользователя
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('join_service.html')
        
        # Проверка, есть ли уже пользователь в этом сервисе
        existing_user = User.query.filter_by(username=username, service_id=service.id).first()
        if existing_user:
            flash('Пользователь уже зарегистрирован в этом сервисе', 'error')
            return render_template('join_service.html')
        
        # Проверка уникальности email (если email не пустой)
        if email and email.strip():
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Пользователь с таким email уже существует', 'error')
                return render_template('join_service.html')
        else:
            # Если email пустой, устанавливаем None вместо пустой строки
            email = None
        
        # Создание пользователя (не подтвержденного)
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role,
            full_name=full_name,
            email=email,
            phone=phone,
            service_id=service.id,
            is_active=True,
            is_approved=False  # Требует подтверждения директора
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Заявка отправлена на подтверждение директору', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('join_service.html')

@service_bp.route('/users')
@login_required
def users():
    """Управление пользователями (только для директора)"""
    if current_user.role != 'director':
        flash('Доступ запрещен', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Получаем всех пользователей сервиса
    users = User.query.filter_by(service_id=current_user.service_id).all()
    pending_users = User.query.filter_by(service_id=current_user.service_id, is_approved=False).all()
    
    return render_template('users.html', users=users, pending_users=pending_users)

@service_bp.route('/api/users/<int:user_id>/approve', methods=['POST'])
@login_required
def approve_user(user_id):
    """Подтверждение пользователя директором"""
    if current_user.role != 'director':
        return jsonify({'success': False, 'message': 'Доступ запрещен'})
    
    user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    user.is_approved = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Пользователь подтвержден'})

@service_bp.route('/api/users/<int:user_id>/reject', methods=['POST'])
@login_required
def reject_user(user_id):
    """Отклонение пользователя директором"""
    if current_user.role != 'director':
        return jsonify({'success': False, 'message': 'Доступ запрещен'})
    
    user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    # Удаляем пользователя
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Пользователь отклонен'})

