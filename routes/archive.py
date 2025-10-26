"""
Маршруты управления архивом
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models.order import Order
from models.device import Device
from models.client import Client
from models.order_status_history import OrderStatusHistory
from models.database import db
from sqlalchemy import or_

archive_bp = Blueprint('archive', __name__)

@archive_bp.route('/archive')
@login_required
def index():
    """Страница архива выданных устройств"""
    service_id = current_user.service_id
    order_id = request.args.get('order_id')
    
    # Получаем все выданные заказы
    issued_orders = Order.query.filter_by(service_id=service_id, status='completed').order_by(Order.updated_at.desc()).all()
    
    # Если указан конкретный заказ, фильтруем по нему
    if order_id:
        issued_orders = [order for order in issued_orders if order.id == int(order_id)]
    
    return render_template('archive.html', issued_orders=issued_orders, highlight_order_id=order_id)

@archive_bp.route('/api/archive', methods=['GET'])
@login_required
def api_archive():
    """API для получения списка выданных заказов"""
    service_id = current_user.service_id
    search_query = request.args.get('q', '')
    
    orders_query = Order.query.filter_by(service_id=service_id, status='completed')
    
    if search_query:
        orders_query = orders_query.join(Device).join(Client).filter(
            or_(
                Device.brand.ilike(f'%{search_query}%'),
                Device.model.ilike(f'%{search_query}%'),
                Device.serial_number.ilike(f'%{search_query}%'),
                Client.name.ilike(f'%{search_query}%')
            )
        )
    
    orders = orders_query.order_by(Order.updated_at.desc()).all()
    
    orders_data = []
    for order in orders:
        order_dict = order.to_dict()
        order_dict['client'] = order.client.to_dict()
        order_dict['device'] = order.device.to_dict()
        orders_data.append(order_dict)
        
    return jsonify(orders_data)

@archive_bp.route('/api/archive/<int:order_id>/history')
@login_required
def get_archive_order_history(order_id):
    """API для получения истории статусов конкретного заказа в архиве"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id, status='completed').first_or_404()
    
    history = OrderStatusHistory.query.filter_by(order_id=order_id).order_by(OrderStatusHistory.created_at.desc()).all()
    
    history_data = []
    for entry in history:
        entry_dict = entry.to_dict()
        entry_dict['new_status_display'] = OrderStatusHistory.get_status_display(entry.new_status)
        entry_dict['old_status_display'] = OrderStatusHistory.get_status_display(entry.old_status) if entry.old_status else None
        history_data.append(entry_dict)
    
    return jsonify(history_data)

@archive_bp.route('/api/archive/<int:order_id>')
@login_required
def get_archive_order(order_id):
    """API для получения данных конкретного заказа из архива"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id, status='completed').first_or_404()
    
    order_dict = order.to_dict()
    order_dict['device'] = order.device.to_dict() if order.device else None
    order_dict['client'] = order.client.to_dict() if order.client else None
    order_dict['device_id'] = order.device_id
    
    return jsonify(order_dict)


