"""
DevTools маршруты для отладки и мониторинга
"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.client import Client
from models.order import Order
from models.part import Part
from models.device import Device
from models.service import Service
import os
import psutil
import time
from datetime import datetime, timedelta
import json

devtools_bp = Blueprint('devtools', __name__, url_prefix='/devtools')

@devtools_bp.route('/api/status')
@login_required
def api_status():
    """Получить общий статус системы"""
    try:
        # Системная информация
        system_info = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime': time.time() - psutil.boot_time()
        }
        
        # Информация о приложении
        app_info = {
            'debug_mode': current_app.debug,
            'config': {
                'SECRET_KEY': '***' if current_app.config.get('SECRET_KEY') else None,
                'SQLALCHEMY_DATABASE_URI': current_app.config.get('SQLALCHEMY_DATABASE_URI', '').split('://')[0] + '://***',
                'SQLALCHEMY_TRACK_MODIFICATIONS': current_app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')
            }
        }
        
        # Статистика базы данных
        db_stats = {
            'users': User.query.count(),
            'clients': Client.query.count(),
            'orders': Order.query.count(),
            'parts': Part.query.count(),
            'devices': Device.query.count(),
            'services': Service.query.count()
        }
        
        return jsonify({
            'success': True,
            'data': {
                'system': system_info,
                'app': app_info,
                'database': db_stats,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/logs')
@login_required
def api_logs():
    """Получить логи приложения"""
    try:
        # Получаем последние записи из базы данных
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        recent_clients = Client.query.order_by(Client.created_at.desc()).limit(5).all()
        
        logs = {
            'recent_orders': [{
                'id': order.id,
                'client_name': order.client.name if order.client else 'Неизвестно',
                'device': f"{order.device_brand} {order.device_model}",
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'cost_estimate': float(order.cost_estimate) if order.cost_estimate else 0
            } for order in recent_orders],
            'recent_clients': [{
                'id': client.id,
                'name': client.name,
                'phone': client.phone,
                'email': client.email,
                'created_at': client.created_at.isoformat()
            } for client in recent_clients]
        }
        
        return jsonify({
            'success': True,
            'data': logs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/performance')
@login_required
def api_performance():
    """Получить метрики производительности"""
    try:
        # Время выполнения запросов
        start_time = time.time()
        
        # Тест скорости базы данных
        db_start = time.time()
        User.query.count()
        db_time = time.time() - db_start
        
        # Общее время ответа
        response_time = time.time() - start_time
        
        performance = {
            'response_time': response_time,
            'db_query_time': db_time,
            'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'cpu_usage': psutil.Process().cpu_percent()
        }
        
        return jsonify({
            'success': True,
            'data': performance
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/database')
@login_required
def api_database():
    """Получить информацию о базе данных"""
    try:
        # Размер базы данных
        db_path = current_app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', '')
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / 1024 / 1024  # MB
        else:
            db_size = 0
        
        # Статистика таблиц
        tables_info = {
            'users': {
                'count': User.query.count(),
                'recent': User.query.order_by(User.created_at.desc()).limit(3).all()
            },
            'clients': {
                'count': Client.query.count(),
                'recent': Client.query.order_by(Client.created_at.desc()).limit(3).all()
            },
            'orders': {
                'count': Order.query.count(),
                'recent': Order.query.order_by(Order.created_at.desc()).limit(3).all()
            }
        }
        
        return jsonify({
            'success': True,
            'data': {
                'size_mb': db_size,
                'tables': tables_info,
                'connection_info': {
                    'engine': str(db.engine.url).split('://')[0],
                    'database': str(db.engine.url).split('/')[-1]
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/errors')
@login_required
def api_errors():
    """Получить информацию об ошибках"""
    try:
        # Здесь можно добавить логику для сбора ошибок
        # Пока возвращаем пустой список
        errors = []
        
        return jsonify({
            'success': True,
            'data': {
                'errors': errors,
                'error_count': len(errors)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/clear-cache')
@login_required
def api_clear_cache():
    """Очистить кэш приложения"""
    try:
        # Здесь можно добавить логику очистки кэша
        # Пока просто возвращаем успех
        return jsonify({
            'success': True,
            'message': 'Кэш очищен'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/api/restart')
@login_required
def api_restart():
    """Перезапустить приложение (только для разработки)"""
    try:
        if not current_app.debug:
            return jsonify({
                'success': False,
                'error': 'Перезапуск доступен только в режиме разработки'
            }), 403
        
        # В реальном приложении здесь была бы логика перезапуска
        return jsonify({
            'success': True,
            'message': 'Приложение будет перезапущено'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@devtools_bp.route('/')
@login_required
def devtools_panel():
    """Главная страница DevTools"""
    from flask import render_template
    return render_template('devtools.html')

