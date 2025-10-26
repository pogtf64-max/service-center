"""
Маршруты управления запчастями
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.part import Part

parts_bp = Blueprint('parts', __name__)

@parts_bp.route('/parts')
@login_required
def index():
    """Страница управления запчастями"""
    parts = Part.query.filter_by(service_id=current_user.service_id).all()
    return render_template('parts.html', parts=parts)

@parts_bp.route('/api/parts', methods=['GET', 'POST'])
@login_required
def api_parts():
    """API для работы с запчастями"""
    if request.method == 'POST':
        data = request.get_json()
        part = Part(
            service_id=current_user.service_id,
            name=data['name'],
            article=data['article'],
            category=data.get('category'),
            quantity=data.get('quantity', 0),
            min_quantity=data.get('min_quantity', 0),
            price=data['price'],
            cost_price=data.get('cost_price'),
            supplier=data.get('supplier'),
            supplier_contact=data.get('supplier_contact'),
            description=data.get('description'),
            specifications=data.get('specifications')
        )
        from models.database import db
        db.session.add(part)
        db.session.commit()
        return jsonify({'success': True, 'id': part.id})
    
    parts = Part.query.filter_by(service_id=current_user.service_id).all()
    return jsonify([part.to_dict() for part in parts])

@parts_bp.route('/api/parts/<int:part_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_part(part_id):
    """API для работы с конкретной запчастью"""
    part = Part.query.filter_by(id=part_id, service_id=current_user.service_id).first_or_404()
    
    if request.method == 'GET':
        return jsonify(part.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        part.name = data.get('name', part.name)
        part.article = data.get('article', part.article)
        part.category = data.get('category', part.category)
        part.quantity = data.get('quantity', part.quantity)
        part.min_quantity = data.get('min_quantity', part.min_quantity)
        part.price = data.get('price', part.price)
        part.cost_price = data.get('cost_price', part.cost_price)
        part.supplier = data.get('supplier', part.supplier)
        part.supplier_contact = data.get('supplier_contact', part.supplier_contact)
        part.description = data.get('description', part.description)
        part.specifications = data.get('specifications', part.specifications)
        part.is_active = data.get('is_active', part.is_active)
        
        from models.database import db
        from datetime import datetime
        part.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        from models.database import db
        db.session.delete(part)
        db.session.commit()
        return jsonify({'success': True})

@parts_bp.route('/api/parts/stock', methods=['GET'])
@login_required
def api_stock_parts():
    """API для получения запчастей со склада для заказа ЗИП"""
    search_query = request.args.get('q', '')
    
    parts_query = Part.query.filter_by(service_id=current_user.service_id, is_active=True)
    
    if search_query:
        parts_query = parts_query.filter(
            Part.name.ilike(f'%{search_query}%') |
            Part.article.ilike(f'%{search_query}%') |
            Part.category.ilike(f'%{search_query}%')
        )
    
    parts = parts_query.order_by(Part.name).all()
    
    parts_data = []
    for part in parts:
        part_dict = part.to_dict()
        part_dict['available_quantity'] = part.quantity
        parts_data.append(part_dict)
    
    return jsonify(parts_data)
