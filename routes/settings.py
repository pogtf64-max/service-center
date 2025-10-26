"""
Маршруты для настроек системы
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.user import User
from models.service import Service
from werkzeug.security import generate_password_hash
import json

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

def check_settings_access():
    """Проверка доступа к настройкам (директор и уполномоченные)"""
    if not current_user.is_authenticated:
        return False
    
    # Директор всегда имеет доступ
    if current_user.role == 'director':
        return True
    
    # Проверяем, есть ли у пользователя права на настройки
    if hasattr(current_user, 'can_manage_settings') and current_user.can_manage_settings:
        return True
    
    return False

@settings_bp.route('/')
@login_required
def index():
    """Главная страница настроек"""
    if not check_settings_access():
        flash('У вас нет прав доступа к настройкам системы', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Получаем всех пользователей сервиса
    users = User.query.filter_by(service_id=current_user.service_id).all()
    
    # Получаем данные сервисного центра
    service = Service.query.get(current_user.service_id)
    
    return render_template('settings.html', users=users, service=service)

@settings_bp.route('/api/service-data')
@login_required
def get_service_data():
    """API для получения данных сервисного центра"""
    try:
        service = Service.query.get(current_user.service_id)
        if not service:
            return jsonify({'success': False, 'message': 'Сервисный центр не найден'}), 404
        
        return jsonify({
            'success': True,
            'service': service.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/update-service', methods=['POST'])
@login_required
def update_service():
    """Обновление реквизитов сервисного центра"""
    if not check_settings_access():
        return jsonify({'success': False, 'message': 'Нет прав доступа'}), 403
    
    try:
        data = request.get_json()
        service = Service.query.get(current_user.service_id)
        
        if not service:
            return jsonify({'success': False, 'message': 'Сервис не найден'}), 404
        
        # Обновляем данные сервиса
        service.name = data.get('name', service.name)
        service.short_name = data.get('short_name', service.short_name)
        service.address = data.get('address', service.address)
        service.legal_address = data.get('legal_address', service.legal_address)
        service.phone = data.get('phone', service.phone)
        service.email = data.get('email', service.email)
        service.website = data.get('website', service.website)
        service.working_hours = data.get('working_hours', service.working_hours)
        
        # Юридические реквизиты
        service.inn = data.get('inn', service.inn)
        service.kpp = data.get('kpp', service.kpp)
        service.ogrn = data.get('ogrn', service.ogrn)
        service.okpo = data.get('okpo', service.okpo)
        service.okved = data.get('okved', service.okved)
        
        # Банковские реквизиты
        service.bank_name = data.get('bank_name', service.bank_name)
        service.bank_bik = data.get('bank_bik', service.bank_bik)
        service.bank_account = data.get('bank_account', service.bank_account)
        service.bank_correspondent_account = data.get('bank_correspondent_account', service.bank_correspondent_account)
        
        # Руководство
        service.director_name = data.get('director_name', service.director_name)
        service.chief_accountant = data.get('chief_accountant', service.chief_accountant)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Реквизиты обновлены'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@settings_bp.route('/update-user-role', methods=['POST'])
@login_required
def update_user_role():
    """Обновление роли пользователя"""
    if not check_settings_access():
        return jsonify({'success': False, 'message': 'Нет прав доступа'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_role = data.get('role')
        
        if not user_id or not new_role:
            return jsonify({'success': False, 'message': 'Не указаны параметры'}), 400
        
        # Проверяем, что пользователь принадлежит к тому же сервису
        user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404
        
        # Нельзя изменить роль директора
        if user.role == 'director':
            return jsonify({'success': False, 'message': 'Нельзя изменить роль директора'}), 400
        
        # Обновляем роль
        user.role = new_role
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Роль обновлена'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@settings_bp.route('/update-user-status', methods=['POST'])
@login_required
def update_user_status():
    """Обновление статуса пользователя (активен/заблокирован)"""
    if not check_settings_access():
        return jsonify({'success': False, 'message': 'Нет прав доступа'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        is_active = data.get('is_active', True)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'Не указан ID пользователя'}), 400
        
        # Проверяем, что пользователь принадлежит к тому же сервису
        user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404
        
        # Нельзя заблокировать директора
        if user.role == 'director':
            return jsonify({'success': False, 'message': 'Нельзя заблокировать директора'}), 400
        
        # Обновляем статус
        user.is_active = is_active
        db.session.commit()
        
        status_text = 'активирован' if is_active else 'заблокирован'
        return jsonify({'success': True, 'message': f'Пользователь {status_text}'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@settings_bp.route('/reset-user-password', methods=['POST'])
@login_required
def reset_user_password():
    """Сброс пароля пользователя"""
    if not check_settings_access():
        return jsonify({'success': False, 'message': 'Нет прав доступа'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_password = data.get('new_password')
        
        if not user_id or not new_password:
            return jsonify({'success': False, 'message': 'Не указаны параметры'}), 400
        
        # Проверяем, что пользователь принадлежит к тому же сервису
        user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404
        
        # Обновляем пароль
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Пароль обновлен'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@settings_bp.route('/update-user-settings-permission', methods=['POST'])
@login_required
def update_user_settings_permission():
    """Обновление разрешения на управление настройками"""
    if not check_settings_access():
        return jsonify({'success': False, 'message': 'Нет прав доступа'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        can_manage = data.get('can_manage', False)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'Не указан ID пользователя'}), 400
        
        # Проверяем, что пользователь принадлежит к тому же сервису
        user = User.query.filter_by(id=user_id, service_id=current_user.service_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404
        
        # Нельзя изменить разрешения директора
        if user.role == 'director':
            return jsonify({'success': False, 'message': 'Нельзя изменить разрешения директора'}), 400
        
        # Обновляем разрешение
        user.can_manage_settings = can_manage
        db.session.commit()
        
        permission_text = 'предоставлено' if can_manage else 'отозвано'
        return jsonify({'success': True, 'message': f'Разрешение на управление настройками {permission_text}'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500
