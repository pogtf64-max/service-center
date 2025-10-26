"""
Маршруты авторизации
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Главная страница"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('welcome.html')

@auth_bp.route('/register-center', methods=['GET', 'POST'])
def register_center():
    """Страница регистрации сервисного центра"""
    if request.method == 'POST':
        # Перенаправляем на обработку в service.py
        return redirect(url_for('service.register_service'))
    return render_template('register_service.html')

@auth_bp.route('/join-center')
def join_center():
    """Страница присоединения к сервису"""
    return render_template('join_service.html')

@auth_bp.route('/select-service', methods=['GET', 'POST'])
def select_service():
    """Страница выбора сервисного центра"""
    if request.method == 'POST':
        service_name = request.form['service_name']
        service_password = request.form['service_password']
        
        # Сохраняем данные сервиса в сессии
        from flask import session
        session['selected_service'] = service_name
        session['service_password'] = service_password
        
        return redirect(url_for('auth.login'))
    
    return render_template('select_service.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в выбранный сервис"""
    from flask import session
    from models.service import Service
    from werkzeug.security import check_password_hash
    
    # Проверяем, выбран ли сервис
    if 'selected_service' not in session:
        return redirect(url_for('auth.select_service'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверяем пароль сервиса
        service = Service.query.filter_by(name=session['selected_service']).first()
        if not service or not check_password_hash(service.service_password, session['service_password']):
            flash('Неверные данные сервисного центра', 'error')
            return redirect(url_for('auth.select_service'))
        
        # Ищем пользователя в этом сервисе
        user = User.query.filter_by(username=username, service_id=service.id).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_approved:
                flash('Ваш аккаунт ожидает подтверждения директора', 'warning')
                return render_template('login.html')
            login_user(user)
            # Очищаем данные сервиса из сессии
            session.pop('selected_service', None)
            session.pop('service_password', None)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('auth.index'))

@auth_bp.route('/modal-demo')
def modal_demo():
    """Демонстрация кастомных модальных окон"""
    return render_template('modal_demo.html')
