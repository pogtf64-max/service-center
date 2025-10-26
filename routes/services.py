"""
Маршруты для управления услугами
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.service_item import ServiceItem
from datetime import datetime

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
@login_required
def index():
    """Страница управления услугами"""
    # Получаем все услуги для текущего сервисного центра
    services = ServiceItem.query.filter_by(service_id=current_user.service_id).all()
    
    return render_template('services.html', services=services)

@services_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add():
    """Добавление новой услуги"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', 0)
            
            if not name:
                flash('Название услуги обязательно', 'error')
                return render_template('add_service.html')
            
            # Создаем новую услугу
            service = ServiceItem(
                name=name,
                description=description,
                price=float(price) if price else 0.0,
                service_id=current_user.service_id,
                is_active=True
            )
            
            db.session.add(service)
            db.session.commit()
            
            flash('Услуга успешно добавлена', 'success')
            return redirect(url_for('services.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении услуги: {str(e)}', 'error')
            return render_template('add_service.html')
    
    return render_template('add_service.html')

@services_bp.route('/api/services/autocomplete')
@login_required
def autocomplete():
    """API для автозаполнения услуг"""
    try:
        services = ServiceItem.query.filter_by(service_id=current_user.service_id, is_active=True).all()
        service_names = [service.name for service in services]
        return jsonify({'services': service_names})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@services_bp.route('/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit(service_id):
    """Редактирование услуги"""
    service = ServiceItem.query.filter_by(id=service_id, service_id=current_user.service_id).first()
    
    if not service:
        flash('Услуга не найдена', 'error')
        return redirect(url_for('services.index'))
    
    if request.method == 'POST':
        try:
            service.name = request.form.get('name', '').strip()
            service.description = request.form.get('description', '').strip()
            service.price = float(request.form.get('price', 0))
            service.is_active = 'is_active' in request.form
            
            db.session.commit()
            flash('Услуга успешно обновлена', 'success')
            return redirect(url_for('services.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении услуги: {str(e)}', 'error')
    
    return render_template('edit_service.html', service=service)

@services_bp.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
def delete(service_id):
    """Удаление услуги"""
    try:
        service = ServiceItem.query.filter_by(id=service_id, service_id=current_user.service_id).first()
        
        if not service:
            return jsonify({'success': False, 'message': 'Услуга не найдена'}), 404
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Услуга успешно удалена'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка при удалении услуги: {str(e)}'}), 500

@services_bp.route('/api/services', methods=['GET'])
@login_required
def api_services():
    """API для получения списка услуг"""
    try:
        services = ServiceItem.query.filter_by(service_id=current_user.service_id, is_active=True).all()
        
        services_data = []
        for service in services:
            services_data.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price
            })
        
        return jsonify({'success': True, 'services': services_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500
