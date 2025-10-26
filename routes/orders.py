"""
Маршруты управления заказами
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.order import Order
from models.client import Client
from models.device import Device
from models.user import User
from models.order_status_history import OrderStatusHistory
from models.cash_register import CashRegister
from models.database import db
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def get_abr_total_cost(device_id):
    """Получить итоговую стоимость всех АВР для устройства"""
    try:
        # Пока что возвращаем 0, так как АВР хранятся в localStorage на клиенте
        # В будущем можно будет добавить серверное хранение АВР
        return 0.0
        
    except Exception as e:
        print(f"Ошибка при получении стоимости АВР: {e}")
        return 0.0

@orders_bp.route('/orders')
@login_required
def index():
    """Страница управления заказами"""
    # Показываем только заказы в определенных статусах (исключаем 'rejected')
    allowed_statuses = ['received', 'requires_approval', 'parts_order', 'parts_ordered', 'ready']
    orders = Order.query.filter_by(service_id=current_user.service_id)\
                       .filter(Order.status.in_(allowed_statuses))\
                       .order_by(Order.created_at.desc()).all()
    
    return render_template('orders.html', orders=orders)

@orders_bp.route('/api/devices/types/search')
@login_required
def search_device_types():
    """Поиск типов устройств"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    # Получаем уникальные типы устройств из базы
    types = db.session.query(Device.type).filter_by(service_id=current_user.service_id)\
                                        .filter(Device.type.ilike(f'%{query}%'))\
                                        .distinct().limit(5).all()
    
    return jsonify([type[0] for type in types])

@orders_bp.route('/api/devices/brands/search')
@login_required
def search_device_brands():
    """Поиск брендов устройств"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    # Получаем уникальные бренды из базы
    brands = db.session.query(Device.brand).filter_by(service_id=current_user.service_id)\
                                          .filter(Device.brand.ilike(f'%{query}%'))\
                                          .distinct().limit(5).all()
    
    return jsonify([brand[0] for brand in brands])

@orders_bp.route('/api/devices/models/search')
@login_required
def search_device_models():
    """Поиск моделей устройств"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    # Получаем уникальные модели из базы
    models = db.session.query(Device.model).filter_by(service_id=current_user.service_id)\
                                          .filter(Device.model.ilike(f'%{query}%'))\
                                          .distinct().limit(5).all()
    
    return jsonify([model[0] for model in models])

@orders_bp.route('/api/orders', methods=['GET', 'POST'])
@login_required
def api_orders():
    """API для работы с заказами"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Создаем или находим клиента
        client = Client.query.filter_by(
            service_id=current_user.service_id,
            name=data['client_name'],
            phone=data['client_phone']
        ).first()
        
        if not client:
            # Создаем нового клиента
            client = Client(
                service_id=current_user.service_id,
                client_type=data.get('client_type', 'individual'),
                name=data['client_name'],
                phone=data['client_phone'],
                email=data.get('client_email'),
                address=data['client_address'],
                organization_name=data.get('organization_name'),
                inn=data.get('inn')
            )
            db.session.add(client)
            db.session.flush()  # Получаем ID клиента
        
        # Создаем устройство
        device = Device(
            service_id=current_user.service_id,
            client_id=client.id,
            device_type=data['device_type'],
            brand=data['device_brand'],
            model=data['device_model'],
            serial_number=data.get('device_serial_number', ''),
            imei=data.get('device_imei', ''),
            condition=data.get('device_condition', ''),
            external_description='',  # Оставляем пустым, так как поле убрано из формы
            completeness=data.get('completeness', '')
        )
        db.session.add(device)
        db.session.flush()  # Получаем ID устройства
        
        # Создаем заказ
        order = Order(
            service_id=current_user.service_id,
            device_id=device.id,
            client_id=client.id,
            problem_description=data['problem_description'],
            cost_estimate=data.get('cost_estimate', 0),
            master_id=data.get('master_id')
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'success': True, 'id': order.id})
    
    orders = Order.query.filter_by(service_id=current_user.service_id).all()
    return jsonify([order.to_dict() for order in orders])

@orders_bp.route('/api/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_order(order_id):
    """API для работы с конкретным заказом"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id).first_or_404()
    
    if request.method == 'GET':
        # Получаем полные данные заказа с связанными объектами
        order_data = order.to_dict()
        
        
        # Добавляем данные сервисного центра (не включен в to_dict())
        if order.service:
            order_data['service'] = order.service.to_dict()
        
        return jsonify(order_data)
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            
            # Обновляем поля заказа
            if 'problem_description' in data:
                order.problem_description = data.get('problem_description')
            if 'diagnosis' in data:
                order.diagnosis = data.get('diagnosis')
            if 'repair_description' in data:
                order.repair_description = data.get('repair_description')
            if 'notes' in data:
                order.notes = data.get('notes')
            
            # Обрабатываем числовые поля
            if 'cost_estimate' in data:
                cost_estimate = data.get('cost_estimate')
                if cost_estimate and cost_estimate.strip():
                    order.cost_estimate = float(cost_estimate)
                else:
                    order.cost_estimate = None
                    
            if 'final_cost' in data:
                final_cost = data.get('final_cost')
                if final_cost and final_cost.strip():
                    order.final_cost = float(final_cost)
                else:
                    order.final_cost = None
                    
            if 'prepayment' in data:
                prepayment = data.get('prepayment')
                if prepayment and prepayment.strip():
                    order.prepayment = float(prepayment)
                else:
                    order.prepayment = None
            
            # Обновляем данные клиента
            if order.client:
                if 'client_name' in data:
                    order.client.name = data.get('client_name')
                if 'client_phone' in data:
                    order.client.phone = data.get('client_phone')
                if 'client_email' in data:
                    order.client.email = data.get('client_email')
            
            # Обновляем данные устройства
            if order.device:
                if 'device_type' in data:
                    order.device.device_type = data.get('device_type')
                if 'device_brand' in data:
                    order.device.brand = data.get('device_brand')
                if 'device_model' in data:
                    order.device.model = data.get('device_model')
                if 'device_serial' in data:
                    order.device.serial_number = data.get('device_serial')
            
            order.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'message': 'Заказ успешно обновлен'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Ошибка обновления заказа: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({'success': True})

@orders_bp.route('/api/orders/<int:order_id>/change-status', methods=['POST'])
@login_required
def change_order_status(order_id):
    """API для изменения статуса заказа"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id).first_or_404()
    
    data = request.get_json()
    new_status = data.get('new_status')
    comment = data.get('comment', '')
    diagnosis_cost = data.get('diagnosis_cost', 500)  # Сумма диагностики для отказов от ремонта
    abr_total = data.get('abr_total', 0.0)  # Итоговая стоимость АВР
    
    if not new_status:
        return jsonify({'success': False, 'message': 'Статус не указан'})
    
    # Сохраняем старый статус
    old_status = order.status
    
    # Специальная логика для статуса "Требуется согласование"
    if old_status == 'requires_approval' and new_status == 'approved':
        # Проверяем всю историю заказа на наличие запчастей и услуг
        has_parts = False
        has_services = False
        
        # Получаем все записи истории для этого заказа
        history_records = OrderStatusHistory.query.filter_by(order_id=order.id)\
                                                 .order_by(OrderStatusHistory.created_at.desc()).all()
        
        # Анализируем записи истории
        for record in history_records:
            if record.comment:
                if 'Запчасти:' in record.comment or 'Заказ ЗИП' in record.comment:
                    has_parts = True
                if 'Услуги:' in record.comment:
                    has_services = True
        
        # Определяем статус на основе содержимого
        if has_parts:
            new_status = 'parts_ordered'
            comment += '\n\nАвтоматический переход: ЗИП заказан (есть запчасти)'
        elif has_services:
            new_status = 'approved'
            comment += '\n\nАвтоматический переход: Согласовано (только услуги)'
        else:
            # Если нет ни запчастей, ни услуг, оставляем как есть
            new_status = 'approved'
            comment += '\n\nАвтоматический переход: Согласовано'
    
    # Создаем запись в истории
    status_history = OrderStatusHistory(
        order_id=order.id,
        user_id=current_user.id,
        old_status=old_status,
        new_status=new_status,
        comment=comment
    )
    
    # Обновляем статус заказа
    order.status = new_status
    order.updated_at = datetime.utcnow()
    
    # Если статус изменился на "Выдано", добавляем деньги в кассу
    # НО ТОЛЬКО для физических лиц (individual), для юридических лиц (legal) деньги в кассу не попадают
    if new_status == 'completed' and old_status != 'completed':
        # Проверяем тип клиента - только для физических лиц добавляем в кассу
        if order.client.client_type == 'individual':
            # Проверяем, есть ли в истории статус "Отказ от ремонта"
            has_rejection_status = OrderStatusHistory.query.filter_by(
                order_id=order.id, 
                new_status='rejected'
            ).first() is not None
            
            if has_rejection_status:
                # Для отказов от ремонта в кассу попадает только сумма диагностики
                # Используем сохраненную сумму диагностики из базы данных
                saved_diagnosis_cost = order.diagnosis_cost or 500.0
                
                # Создаем запись в кассе только с суммой диагностики
                cash_entry = CashRegister(
                    service_id=current_user.service_id,
                    user_id=current_user.id,
                    order_id=order.id,
                    amount=saved_diagnosis_cost,
                    description=f"Заказ #{order.id} - Диагностика (отказ от ремонта) - {order.device.brand} {order.device.model}"
                )
                db.session.add(cash_entry)
            else:
                # Для обычных заказов используем полную стоимость
                order_cost = order.final_cost or order.cost_estimate or 0
                
                # Получаем итоговую стоимость из АВР (переданную от клиента)
                try:
                    abr_total = float(abr_total)
                except (ValueError, TypeError):
                    abr_total = 0.0
                
                # Используем большую из двух сумм: стоимость заказа или АВР
                final_amount = max(order_cost, abr_total)
                
                if final_amount > 0:
                    # Создаем запись в кассе
                    description = f"Заказ #{order.id} - {order.device.brand} {order.device.model}"
                    if abr_total > order_cost:
                        description += f" (АВР: {abr_total:.2f} ₽)"
                    
                    cash_entry = CashRegister(
                        service_id=current_user.service_id,
                        user_id=current_user.id,
                        order_id=order.id,
                        amount=final_amount,
                        description=description
                    )
                    db.session.add(cash_entry)
        # Для юридических лиц (client_type == 'legal') деньги в кассу НЕ добавляем
    
    db.session.add(status_history)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Статус успешно изменен',
        'new_status': new_status,
        'new_status_display': order.get_status_display()
    })

@orders_bp.route('/api/orders/<int:order_id>/status-history')
@login_required
def get_order_status_history(order_id):
    """API для получения истории статусов заказа"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id).first_or_404()
    
    history = OrderStatusHistory.query.filter_by(order_id=order_id).order_by(OrderStatusHistory.created_at.desc()).all()
    
    history_data = []
    for entry in history:
        entry_dict = entry.to_dict()
        entry_dict['new_status_display'] = OrderStatusHistory.get_status_display(entry.new_status)
        entry_dict['old_status_display'] = OrderStatusHistory.get_status_display(entry.old_status) if entry.old_status else None
        history_data.append(entry_dict)
    
    return jsonify(history_data)

@orders_bp.route('/api/orders/<int:order_id>/abr-total', methods=['POST'])
@login_required
def get_abr_total_for_order(order_id):
    """API для получения итоговой стоимости АВР для заказа"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id).first_or_404()
    
    data = request.get_json()
    abr_total = data.get('abr_total', 0.0)
    
    try:
        abr_total = float(abr_total)
        return jsonify({
            'success': True,
            'abr_total': abr_total
        })
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'Некорректная сумма АВР'
        }), 400

@orders_bp.route('/api/orders/<int:order_id>/save-diagnosis-cost', methods=['POST'])
@login_required
def save_diagnosis_cost(order_id):
    """API для сохранения суммы диагностики для заказов с отказом от ремонта"""
    order = Order.query.filter_by(id=order_id, service_id=current_user.service_id).first_or_404()
    
    data = request.get_json()
    diagnosis_cost = data.get('diagnosis_cost', 500.0)
    
    # Проверяем, что заказ имеет статус "Отказ от ремонта" в истории
    has_rejection_status = OrderStatusHistory.query.filter_by(
        order_id=order_id, 
        new_status='rejected'
    ).first() is not None
    
    if not has_rejection_status:
        return jsonify({
            'success': False,
            'message': 'Этот заказ не имеет статуса "Отказ от ремонта"'
        }), 400
    
    # Сохраняем сумму диагностики
    order.diagnosis_cost = float(diagnosis_cost)
    order.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Сумма диагностики успешно сохранена',
        'diagnosis_cost': order.diagnosis_cost
    })
