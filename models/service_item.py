"""
Модель услуги сервисного центра
"""
from datetime import datetime
from .database import db

class ServiceItem(db.Model):
    """Модель услуги сервисного центра"""
    __tablename__ = 'service_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    service = db.relationship('Service', backref='service_items')
    
    def __repr__(self):
        return f'<ServiceItem {self.name}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'service_id': self.service_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

