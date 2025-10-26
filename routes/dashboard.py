"""
Маршруты панели управления
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.order import Order
from models.client import Client
from models.cash_register import CashRegister
from models.service import Service
from models.database import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Панель управления"""
    # Получаем информацию о сервисном центре
    service = Service.query.get(current_user.service_id)
    
    # Получаем статистику для текущего сервиса
    orders_in_progress = Order.query.filter_by(service_id=current_user.service_id).filter(Order.status.in_(['received', 'diagnosis', 'repair'])).count()
    ready_orders = Order.query.filter_by(service_id=current_user.service_id, status='ready').count()
    total_clients = Client.query.filter_by(service_id=current_user.service_id).count()
    total_orders = Order.query.filter_by(service_id=current_user.service_id).count()
    
    # Получаем данные кассы
    total_cash = CashRegister.get_total_amount(current_user.service_id)
    today_cash = CashRegister.get_today_amount(current_user.service_id)
    
    # Последние заказы
    recent_orders = Order.query.filter_by(service_id=current_user.service_id).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         service=service,
                         orders_in_progress=orders_in_progress,
                         ready_orders=ready_orders,
                         total_clients=total_clients,
                         total_orders=total_orders,
                         total_cash=total_cash,
                         today_cash=today_cash,
                         recent_orders=recent_orders)

@dashboard_bp.route('/api/cash/add', methods=['POST'])
@login_required
def add_cash():
    """API для добавления денег в кассу"""
    try:
        data = request.get_json()
        amount = data.get('amount', 0)
        description = data.get('description', '')
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Сумма должна быть больше 0'}), 400
        
        if not description.strip():
            return jsonify({'success': False, 'message': 'Описание не может быть пустым'}), 400
        
        # Создаем запись в кассе
        cash_entry = CashRegister(
            service_id=current_user.service_id,
            user_id=current_user.id,
            amount=amount,
            description=description.strip()
        )
        
        db.session.add(cash_entry)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Деньги успешно добавлены в кассу',
            'amount': amount
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@dashboard_bp.route('/api/cash/subtract', methods=['POST'])
@login_required
def subtract_cash():
    """API для убавления денег из кассы"""
    try:
        data = request.get_json()
        amount = data.get('amount', 0)
        description = data.get('description', '')
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Сумма должна быть больше 0'}), 400
        
        if not description.strip():
            return jsonify({'success': False, 'message': 'Описание не может быть пустым'}), 400
        
        # Проверяем, что в кассе достаточно денег
        current_total = CashRegister.get_total_amount(current_user.service_id)
        if current_total < amount:
            return jsonify({'success': False, 'message': f'Недостаточно средств в кассе. Доступно: {current_total:.2f} ₽'}), 400
        
        # Создаем запись в кассе с отрицательной суммой
        cash_entry = CashRegister(
            service_id=current_user.service_id,
            user_id=current_user.id,
            amount=-amount,  # Отрицательная сумма для убавления
            description=description.strip()
        )
        
        db.session.add(cash_entry)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Деньги успешно убраны из кассы',
            'amount': amount
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'}), 500

@dashboard_bp.route('/cash-history')
@login_required
def cash_history():
    """Страница истории кассы"""
    # Получаем все записи кассы для текущего сервиса с загрузкой пользователей
    cash_entries = CashRegister.query.filter_by(service_id=current_user.service_id)\
                                   .join(CashRegister.user, isouter=True)\
                                   .order_by(CashRegister.created_at.desc()).all()
    
    # Получаем общую сумму
    total_cash = CashRegister.get_total_amount(current_user.service_id)
    
    return render_template('cash_history.html', 
                         cash_entries=cash_entries,
                         total_cash=total_cash)
