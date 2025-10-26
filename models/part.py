"""
Модель запчасти
"""
from datetime import datetime
from .database import db

class Part(db.Model):
    """Модель запчасти"""
    __tablename__ = 'parts'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    article = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50))
    
    # Количество и цены
    quantity = db.Column(db.Integer, default=0)
    min_quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float)
    
    # Поставщик
    supplier = db.Column(db.String(100))
    supplier_contact = db.Column(db.String(200))
    
    # Описание
    description = db.Column(db.Text)
    specifications = db.Column(db.Text)
    
    # Статус
    is_active = db.Column(db.Boolean, default=True)
    
    # Даты
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Part {self.name}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'name': self.name,
            'article': self.article,
            'category': self.category,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'price': self.price,
            'cost_price': self.cost_price,
            'supplier': self.supplier,
            'supplier_contact': self.supplier_contact,
            'description': self.description,
            'specifications': self.specifications,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def is_low_stock(self):
        """Проверка на низкий остаток"""
        return self.quantity <= self.min_quantity
