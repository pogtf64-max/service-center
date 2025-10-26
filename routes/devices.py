"""
НОВЫЙ файл routes/devices.py с исправленной функцией order_parts
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.device import Device
from models.client import Client
from models.order import Order
from models.order_status_history import OrderStatusHistory
from models.part import Part
from models.service import Service
from models.database import db
from datetime import datetime

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices')
@login_required
def index():
    """Страница управления устройствами"""
    return render_template('devices.html')

@devices_bp.route('/api/devices')
@login_required
def api_devices():
    """API для получения списка устройств"""
    devices = Device.query.filter_by(service_id=current_user.service_id).all()
    devices_data = []
    
    for device in devices:
        # Получаем последний заказ для устройства
        latest_order = Order.query.filter_by(device_id=device.id, service_id=current_user.service_id)\
                                 .order_by(Order.created_at.desc()).first()
        
        # Получаем первый заказ для получения оригинального описания проблемы
        first_order = Order.query.filter_by(device_id=device.id, service_id=current_user.service_id)\
                                .order_by(Order.created_at.asc()).first()
        
        # Исключаем устройства с завершенными или ожидающими статусами
        excluded_statuses = [
            'requires_approval',  # Требуется согласование
            'approved',          # Согласовано
            'ready',             # Готов к выдаче
            'parts_order',       # Заказ ЗИП
            'parts_ordered',     # ЗИП заказан
            # 'parts_issued',    # ЗИП выдан - убрано из исключений
            'completed',         # Выдано
            'rejected'           # Отказ от ремонта
        ]
        
        if latest_order and latest_order.status in excluded_statuses:
            continue
        
        device_dict = device.to_dict()
        device_dict['client_name'] = device.client.name if device.client else 'Не указан'
        device_dict['latest_order_status'] = latest_order.get_status_display() if latest_order else None
        device_dict['latest_order_id'] = latest_order.id if latest_order else None
        device_dict['problem_description'] = first_order.problem_description if first_order else None
        devices_data.append(device_dict)
    
    return jsonify(devices_data)

@devices_bp.route('/api/devices/<int:device_id>')
@login_required
def api_device_detail(device_id):
    """API для получения детальной информации об устройстве"""
    device = Device.query.filter_by(id=device_id, service_id=current_user.service_id).first()
    if not device:
        return jsonify({'error': 'Устройство не найдено'}), 404
    
    # Получаем последний заказ для устройства
    latest_order = Order.query.filter_by(device_id=device.id, service_id=current_user.service_id)\
                             .order_by(Order.created_at.desc()).first()
    
    # Получаем первый заказ для получения оригинального описания проблемы
    first_order = Order.query.filter_by(device_id=device.id, service_id=current_user.service_id)\
                            .order_by(Order.created_at.asc()).first()
    
    device_dict = device.to_dict()
    device_dict['client'] = device.client.to_dict() if device.client else None
    device_dict['latest_order_status'] = latest_order.get_status_display() if latest_order else None
    device_dict['problem_description'] = first_order.problem_description if first_order else None
    
    return jsonify(device_dict)

@devices_bp.route('/api/devices/<int:device_id>/existing-parts', methods=['GET'])
@login_required
def get_existing_parts(device_id):
    """API для получения существующих запчастей и услуг из заказа на согласовании"""
    device = Device.query.filter_by(id=device_id, service_id=current_user.service_id).first()
    if not device:
        return jsonify({'error': 'Устройство не найдено'}), 404
    
    # Ищем заказ с ЗИП в любом статусе
    orders_with_parts = Order.query.filter_by(device_id=device_id, service_id=current_user.service_id).all()
    
    # Ищем заказ с комментарием о ЗИП
    order_with_parts = None
    for order in orders_with_parts:
        history_entry = OrderStatusHistory.query.filter_by(order_id=order.id)\
                                               .filter(OrderStatusHistory.comment.like('%Заказ ЗИП создан%'))\
                                               .first()
        if history_entry:
            order_with_parts = order
            break
    
    if not order_with_parts:
        return jsonify({
            'parts': [],
            'services': [],
            'total_cost': 0,
            'notes': '',
            'debug': 'No order with parts found'
        })
    
    # Парсим комментарий из истории статусов
    history_entry = OrderStatusHistory.query.filter_by(order_id=order_with_parts.id)\
                                           .filter(OrderStatusHistory.comment.like('%Заказ ЗИП создан%'))\
                                           .first()
    
    parts = []
    services = []
    total_cost = 0
    
    if history_entry and history_entry.comment:
        # Парсим запчасти и услуги из комментария
        import re
        
        # Используем ту же логику парсинга, что и в get_ordered_parts
        # Парсим запчасти в формате "• название - количество шт. × цена ₽ = общая_цена ₽"
        parts_pattern = r'•\s*([^•]+?)\s*-\s*(\d+)\s*шт\.\s*×\s*([\d.]+)\s*₽\s*=\s*([\d.]+)\s*₽'
        parts_matches = re.findall(parts_pattern, history_entry.comment, re.MULTILINE | re.DOTALL)
        
        for match in parts_matches:
            name, quantity, price, total = match
            parts.append({
                'name': name.strip(),
                'quantity': int(quantity),
                'price': float(price),
                'total': float(total)
            })
            total_cost += float(total)
        
        # Парсим услуги в формате "• название - цена ₽"
        services_pattern = r'•\s*([^•\n]+?)\s*-\s*(\d+)\s*₽'
        services_matches = re.findall(services_pattern, history_entry.comment, re.MULTILINE | re.DOTALL)
        
        for service_name, price in services_matches:
            services.append({
                'name': service_name.strip(),
                'quantity': 1,
                'price': float(price),
                'total': float(price)
            })
            total_cost += float(price)
    
    return jsonify({
        'parts': parts,
        'services': services,
        'total_cost': total_cost,
        'notes': f'Заказ №{order_with_parts.id} от {order_with_parts.created_at.strftime("%d.%m.%Y")}',
        'debug': f'Found {len(parts)} parts and {len(services)} services'
    })

@devices_bp.route('/api/devices/order-parts', methods=['POST'])
@login_required
def order_parts():
    """API для заказа запчастей"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        parts = data.get('parts', [])
        services = data.get('services', [])
        
        if not device_id:
            return jsonify({'error': 'Не указан ID устройства'}), 400
        
        device = Device.query.filter_by(id=device_id, service_id=current_user.service_id).first()
        if not device:
            return jsonify({'error': 'Устройство не найдено'}), 404
        
        # Находим оригинальный заказ устройства для получения описания проблемы
        original_order = Order.query.filter_by(device_id=device_id, service_id=current_user.service_id)\
                                  .order_by(Order.created_at.asc()).first()
        
        # Создаем заказ ЗИП - ИСПРАВЛЕНО
        order = Order(
            device_id=device_id,
            service_id=current_user.service_id,
            client_id=device.client_id,
            status='requires_approval',
            problem_description=original_order.problem_description if original_order else 'Заказ ЗИП'
        )
        db.session.add(order)
        db.session.flush()  # Получаем ID заказа
        
        # Формируем комментарий для истории
        parts_text = ""
        services_text = ""
        total_cost = 0
        
        if parts:
            parts_list = []
            for p in parts:
                if isinstance(p, dict):
                    name = p.get('name', 'Неизвестная запчасть')
                    quantity = p.get('quantity', 1)
                    price = p.get('price', 0)
                    total = quantity * price
                    total_cost += total
                    parts_list.append(f"• {name} - {quantity} шт. × {price} ₽ = {total} ₽")
                else:
                    parts_list.append(f"• {p}")
            parts_text = "Запчасти: " + ", ".join(parts_list)
        
        if services:
            services_list = []
            for s in services:
                if isinstance(s, dict):
                    name = s.get('name', 'Неизвестная услуга')
                    price = s.get('price', 0)
                    total_cost += price
                    services_list.append(f"• {name} - {price} ₽")
                else:
                    services_list.append(f"• {s}")
            services_text = "Услуги: " + ", ".join(services_list)
        
        # Формируем комментарий только из непустых частей
        comment_parts = []
        if parts_text:
            comment_parts.append(parts_text)
        if services_text:
            comment_parts.append(services_text)
        if total_cost > 0:
            comment_parts.append(f"Общая стоимость: {total_cost} ₽")
        
        comment = f'Заказ ЗИП создан. Требуется согласование. {" ".join(comment_parts)}'
        
        # Создаем запись в истории статусов
        history_entry = OrderStatusHistory(
            order_id=order.id,
            user_id=current_user.id,
            old_status=None,
            new_status='requires_approval',
            comment=comment
        )
        db.session.add(history_entry)
        
        db.session.commit()
        print("=== ЗАКАЗ ЗИП УСПЕШНО СОЗДАН ===")
        return jsonify({'success': True, 'message': 'Заказ ЗИП создан'})
        
    except Exception as e:
        print(f"=== ОШИБКА В ORDER_PARTS: {str(e)} ===")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@devices_bp.route('/api/devices/<int:device_id>/status-history')
@login_required
def get_device_status_history(device_id):
    """Получение истории статусов устройства"""
    device = Device.query.filter_by(id=device_id, service_id=current_user.service_id).first()
    if not device:
        return jsonify({'error': 'Устройство не найдено'}), 404
    
    # Получаем все заказы для устройства
    orders = Order.query.filter_by(device_id=device_id, service_id=current_user.service_id).all()
    
    # Получаем историю статусов для всех заказов
    history_data = []
    for order in orders:
        history_entries = OrderStatusHistory.query.filter_by(order_id=order.id)\
                                                 .order_by(OrderStatusHistory.created_at.desc()).all()
        
        for entry in history_entries:
            entry_dict = entry.to_dict()
            entry_dict['new_status_display'] = OrderStatusHistory.get_status_display(entry.new_status)
            entry_dict['old_status_display'] = OrderStatusHistory.get_status_display(entry.old_status) if entry.old_status else None
            history_data.append(entry_dict)
    
    return jsonify(history_data)

@devices_bp.route('/api/devices/<int:device_id>/ordered-parts')
@login_required
def get_ordered_parts(device_id):
    """Получение заказанных запчастей для устройства"""
    device = Device.query.filter_by(id=device_id, service_id=current_user.service_id).first()
    if not device:
        return jsonify({'error': 'Устройство не найдено'}), 404
    
    # Получаем последний заказ для устройства
    latest_order = Order.query.filter_by(device_id=device_id, service_id=current_user.service_id)\
                             .order_by(Order.created_at.desc()).first()
    
    if not latest_order:
        return jsonify({'parts': [], 'services': []})
    
    # Получаем историю статусов для заказа
    history_entries = OrderStatusHistory.query.filter_by(order_id=latest_order.id)\
                                             .order_by(OrderStatusHistory.created_at.desc()).all()
    
    parts = []
    services = []
    
    for entry in history_entries:
        if entry.comment and 'Заказ ЗИП' in entry.comment:
            print(f"=== ПАРСИНГ ЗАКАЗАННЫХ ЗАПЧАСТЕЙ ===")
            print(f"Комментарий: {entry.comment}")
            # Парсим запчасти из комментария
            import re
            
            # Ищем запчасти в формате "• название - количество шт. × цена ₽ = общая_цена ₽"
            # Обновленный паттерн для более гибкого парсинга с поддержкой многострочности
            # Используем более точный паттерн для названий с возможными переносами
            parts_pattern = r'•\s*([^•]+?)\s*-\s*(\d+)\s*шт\.\s*×\s*([\d.]+)\s*₽\s*=\s*([\d.]+)\s*₽'
            parts_matches = re.findall(parts_pattern, entry.comment, re.MULTILINE | re.DOTALL)
            
            # Если не нашли по основному паттерну, пробуем альтернативный формат
            if not parts_matches:
                alt_pattern = r'•\s*([^-\n]+?)\s*-\s*(\d+)\s*шт\.\s*×\s*([\d.]+)\s*P\s*=\s*([\d.]+)\s*P'
                parts_matches = re.findall(alt_pattern, entry.comment, re.MULTILINE)
            
            print(f"Найдено запчастей: {len(parts_matches)}")
            for i, match in enumerate(parts_matches):
                print(f"Запчасть {i+1}: {match}")
            
            for match in parts_matches:
                name, quantity, price, total = match
                parts.append({
                    'name': name.strip(),
                    'quantity': int(quantity),
                    'price': float(price),
                    'total': float(total)
                })
            
            # Ищем услуги в формате "• название - цена ₽" после "Услуги:"
            # Используем более простой подход - ищем все услуги в комментарии
            services_pattern = r'•\s*([^•\n]+?)\s*-\s*(\d+)\s*₽'
            services_matches = re.findall(services_pattern, entry.comment, re.MULTILINE | re.DOTALL)
            print(f"Найдено услуг по паттерну: {len(services_matches)}")
            for i, match in enumerate(services_matches):
                print(f"Услуга {i+1}: {match}")
            
            for service_name, price in services_matches:
                services.append({
                    'name': service_name.strip(),
                    'quantity': 1,
                    'price': float(price),
                    'total': float(price)
                })
    
    return jsonify({'parts': parts, 'services': services})
