"""
Маршруты управления клиентами
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.client import Client
from models.device import Device
from datetime import datetime

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/clients')
@login_required
def index():
    """Страница управления клиентами"""
    clients = Client.query.filter_by(service_id=current_user.service_id).all()
    return render_template('clients.html', clients=clients)

@clients_bp.route('/api/clients/search')
@login_required
def search_clients():
    """Поиск клиентов по имени"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    clients = Client.query.filter_by(service_id=current_user.service_id)\
                         .filter(Client.name.ilike(f'%{query}%'))\
                         .limit(5).all()
    
    return jsonify([{
        'id': client.id,
        'name': client.name,
        'phone': client.phone,
        'email': client.email,
        'address': client.address,
        'created_at': client.created_at.isoformat()
    } for client in clients])

@clients_bp.route('/api/clients', methods=['GET', 'POST'])
@login_required
def api_clients():
    """API для работы с клиентами"""
    if request.method == 'POST':
        data = request.get_json()
        client = Client(
            service_id=current_user.service_id,
            client_type=data.get('client_type', 'individual'),
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            address=data.get('address'),
            organization_name=data.get('organization_name'),
            inn=data.get('inn'),
            notes=data.get('notes')
        )
        from models.database import db
        db.session.add(client)
        db.session.commit()
        return jsonify({'success': True, 'id': client.id})
    
    clients = Client.query.filter_by(service_id=current_user.service_id).all()
    return jsonify([client.to_dict() for client in clients])

@clients_bp.route('/api/clients/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_client(client_id):
    """API для работы с конкретным клиентом"""
    client = Client.query.filter_by(id=client_id, service_id=current_user.service_id).first_or_404()
    
    if request.method == 'GET':
        return jsonify(client.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        client.name = data.get('name', client.name)
        client.phone = data.get('phone', client.phone)
        client.email = data.get('email', client.email)
        client.address = data.get('address', client.address)
        client.notes = data.get('notes', client.notes)
        client.updated_at = datetime.utcnow()
        
        from models.database import db
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        from models.database import db
        db.session.delete(client)
        db.session.commit()
        return jsonify({'success': True})
